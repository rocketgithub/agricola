# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
import logging
from odoo.addons import decimal_precision as dp

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    domingos = fields.Integer(compute='_get_domingos_trabajados',string='Domingos Trabajados')

    def _get_domingos_trabajados(self):
        cantidad_domingos = 0
        contador = 0
        for payslip in self:
            fecha_desde =  datetime.datetime.strptime(str(payslip.date_from),"%Y-%m-%d")
            fecha_hasta = datetime.datetime.strptime(str(payslip.date_to),"%Y-%m-%d")
            now = datetime.datetime.now()
            cantidad_dias = fecha_hasta - fecha_desde
            cantidad_dias = cantidad_dias.days
            dias_a_trabajar = 0
            while (contador <= cantidad_dias):
                otro_tiempo  = fecha_desde + datetime.timedelta(days = contador)
                if (otro_tiempo.strftime("%A") == 'Sunday'):
                    cantidad_domingos += 1
                contador +=1
            payslip.domingos = cantidad_domingos

    def get_worked_day_task_lines(self,contract, empleado_id, date_from, date_to):
        lista = []
        self.env.cr.execute('select al.date,sum(al.unit_amount) as unit_amount, sum(pt.valor_a_pagar * al.unit_amount) as valor_a_pagar,al.task_id, al.empleado_id,pt.name,pt.codigo '\
            'from account_analytic_line al join project_task pt on(pt.id = al.task_id) where al.employee_id = %s and al.date >=%s and al.date <= %s'\
            'group by al.task_id,al.date,al.empleado_id,pt.name, pt.codigo',(empleado_id,str(date_from),str(date_to)))
        for i in self.env.cr.dictfetchall():
            linea = {
                'task_id': i['task_id'],
                'date': i['date'],
                'task_name': i['name'],
                'code': i['codigo'],
                'dias_trabajados': 1,
                'horas_trabajadas': i['unit_amount'],
                'amount': i['valor_a_pagar'],
            }
            lista.append(linea)
        lineas_resumidas = {}
        for i in lista:
            llave = i['task_id']
            if llave not in lineas_resumidas:
                lineas_resumidas[llave] = dict(i)
                lineas_resumidas[llave]['task_name'] = i['task_name']
                lineas_resumidas[llave]['code'] = i['code']
            else:
                lineas_resumidas[llave]['dias_trabajados'] += i['dias_trabajados']
                lineas_resumidas[llave]['horas_trabajadas'] += i['horas_trabajadas']
                lineas_resumidas[llave]['amount'] += i['amount']
        lineas = lineas_resumidas.values()
        return lineas

    def compute_sheet(self):
        for nomina in self:
            if nomina.input_line_ids:
                datos = self.get_worked_day_task_lines(nomina.contract_id.id, nomina.employee_id.id, nomina.date_from, nomina.date_to)
                if datos:
                    for d in datos:
                        for linea in nomina.input_line_ids:
                            if linea.input_type_id.code == d['code']:
                                linea.amount = d['horas_trabajadas']
        res = super(HrPayslip, self).compute_sheet()
        return res

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    asuetos = fields.Integer('Asuetos')

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    unit_amount = fields.Float(digits=dp.get_precision('Payroll Rate'))

class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'

    amount = fields.Float(digits=dp.get_precision('Payroll Rate'))

class HrPayslipWorkedDays(models.Model):
    _inherit = 'hr.payslip.worked_days'

    number_of_hours = fields.Float(digits=dp.get_precision('Payroll Rate'))
