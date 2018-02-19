# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

class Employee(models.Model):
    _inherit = 'hr.employee'

    codigo_empleado = fields.Char('Código del empleado')
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        res1 = super(Employee, self).name_search(name, args, operator=operator, limit=limit)

        records = self.search([('codigo_empleado', 'ilike', name)], limit=limit)
        res2 = records.name_get()

        return res1+res2
