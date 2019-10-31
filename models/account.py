# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging


class Agricola_AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    subarea_id = fields.Many2one('agricola.catalogos.subareas', 'Sub Area')
    area_id = fields.Many2one('agricola.catalogos.areas', related='subarea_id.area_id',store=True,string='Area')
    empleado_id = fields.Many2one('hr.employee', string='Trabajador')
    hora_entrada = fields.Float('Hora de entrada', default=0.0)
    produccion = fields.Float('Producción', digits=(16,2))
    udm_produccion = fields.Many2one('product.uom', string='Unidad de Producción')
    finca_id = fields.Many2one('agricola.catalogos.fincas',related="area_id.finca_id",store=True,string="Finca")
