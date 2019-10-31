# -*- coding: utf-8 -*-

from odoo import models, fields, api
import zeep
import logging

class Fincas(models.Model):
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
    def name_get(self):
        res = []
        for subarea in self:
            name = []
            if subarea.area_id:
                if subarea.area_id.finca_id:
                    name.append(subarea.area_id.finca_id.name or "")
                name.append(subarea.area_id.name or "")
            name.append(subarea.name or "")
            res.append((subarea.id, " - ".join(name)))
        return res

class DuracionTarea(models.Model):
    _name = 'agricola.catalogos.duracion_tarea'

    name = fields.Char("Nombre", required=True)
