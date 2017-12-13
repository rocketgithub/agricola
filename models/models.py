# -*- coding: utf-8 -*-

from odoo import models, fields, api
import zeep
import logging

class fincas(models.Model):
    _name = 'agricola.catalogos.fincas'

    name = fields.Char("Nombre")
    descripcion = fields.Char("Descripcion")
    partner_id = fields.Many2one("res.partner", string='Direccion', ondelete='restrict')
    areas = fields.One2many('agricola.catalogos.areas', 'finca_id', string='Areas')

class Areas(models.Model):
    _name = 'agricola.catalogos.areas'

    name = fields.Char("Nombre")
    descripcion = fields.Char("Descripcion")
    finca_id = fields.Many2one("agricola.catalogos.fincas", string='Finca', ondelete='restrict')
    subareas = fields.One2many('agricola.catalogos.subareas', 'area_id', string='Sub Areas')


class Subareas(models.Model):
    _name = 'agricola.catalogos.subareas'

    name = fields.Char("Nombre")
    descripcion = fields.Char("Descripcion")
    area_id = fields.Many2one("agricola.catalogos.areas", string='Area', ondelete='restrict')

    @api.multi
    @api.depends('name')
    def name_get(self):

        res = []
        for subarea in self:
            name = subarea.name
            res.append((subarea.id, subarea.area_id.finca_id.name + ' - ' + subarea.area_id.name + ' - ' + name))
        return res


class Agricola_AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    subarea_id = fields.Many2one('agricola.catalogos.subareas', 'Sub Area')
    empleado_id = fields.Many2one('hr.employee', string='Trabajador')
    hora_entrada = fields.Integer('Hora de entrada')
