# -*- coding: utf-8 -*-
# from odoo import http


# class Catering(http.Controller):
#     @http.route('/catering/catering/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/catering/catering/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('catering.listing', {
#             'root': '/catering/catering',
#             'objects': http.request.env['catering.catering'].search([]),
#         })

#     @http.route('/catering/catering/objects/<model("catering.catering"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('catering.object', {
#             'object': obj
#         })
