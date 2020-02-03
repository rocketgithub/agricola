# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
import logging

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
        # partes_de_horas = self.env['account.analytic.line'].search([['user_id', '=', user_id],['date','>=',date_from],['date','<=',date_to],['task_id','!=',False]])
        lista = []
        # for i in partes_de_horas:
        #     fechas = {
        #     'task_id': i.task_id.id,
        #     'date': i.date,
        #     }
        #     fechas_lista.append(fechas)
        #     linea = {
        #         'task_id': i.task_id.id,
        #         'date': i.date,
        #         'task_name': i.task_id.name,
        #         'code': i.task_id.codigo,
        #         'dias_trabajados': 1,
        #         'horas_trabajadas': i.unit_amount,
        #         'amount': (i.task_id.valor_a_pagar )* i.unit_amount,
        #     }
        #     lista.append(linea)
        self.env.cr.execute('select al.date,sum(al.unit_amount) as unit_amount, sum(pt.valor_a_pagar * al.unit_amount) as valor_a_pagar,al.task_id, al.empleado_id,pt.name,pt.codigo '\
            'from account_analytic_line al join project_task pt on(pt.id = al.task_id) where al.empleado_id = %s and al.date >=%s and al.date <= %s'\
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
        # for l in lista:
        #     llave = l['task_id']
        #     if llave not in lineas_resumidas:
        #         lineas_resumidas[llave] = dict(l)
        #         lineas_resumidas[llave]['task_name'] = l['task_name']
        #         lineas_resumidas[llave]['code'] = l['code']
        #     else:
        #         lineas_resumidas[llave]['dias_trabajados'] += l['dias_trabajados']
        #         lineas_resumidas[llave]['horas_trabajadas'] += l['horas_trabajadas']
        #         lineas_resumidas[llave]['amount'] += l['amount']

        # lineas = lineas_resumidas.values()
        return lineas

    def get_worked_day_lines(self, contract_ids, date_from, date_to):
        data = super(HrPayslip, self).get_worked_day_lines(contract_ids, date_from, date_to)
        # for contract in self.env['hr.contract'].browse(contract_ids).filtered(lambda contract: contract.resource_calendar_id):
        for contract in contract_ids:
            datos = self.get_worked_day_task_lines(contract.id, contract.employee_id.id, date_from, date_to)
            for i in datos:
                data.append({
                    'name': i['task_name'],
                    'sequence': 10,
                    'code': i['code'],
                    'number_of_days': i['dias_trabajados'],
                    'number_of_hours': i['horas_trabajadas'],
                    'contract_id': contract.id,
                })
        return data


    def get_inputs(self, contract_ids, date_from, date_to):
        res = super(HrPayslip, self).get_inputs(contract_ids, date_from, date_to)
        # for contract in self.env['hr.contract'].browse(contract_ids).filtered(lambda contract: contract.working_hours):
        for contract in contract_ids:
            datos = self.get_worked_day_task_lines(contract.id, contract.employee_id.id, date_from, date_to)
            for r in res:
                for d in datos:
                    if d['code'] == r['code']:
                        r['amount'] = d['amount']
        return res
