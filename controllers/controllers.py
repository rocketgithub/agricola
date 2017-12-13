# -*- coding: utf-8 -*-
from odoo import http

# class Agricola(http.Controller):
#     @http.route('/agricola/agricola/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/agricola/agricola/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('agricola.listing', {
#             'root': '/agricola/agricola',
#             'objects': http.request.env['agricola.agricola'].search([]),
#         })

#     @http.route('/agricola/agricola/objects/<model("agricola.agricola"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('agricola.object', {
#             'object': obj
#         })