# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _

class Task(models.Model):
    _inherit = "project.task"

    valor_a_pagar = fields.Float('Valor a Pagar', digits=(16,2))
