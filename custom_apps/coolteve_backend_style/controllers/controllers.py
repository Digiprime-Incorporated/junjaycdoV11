# -*- coding: utf-8 -*-
from odoo import http

# class CoolteBackendStyle(http.Controller):
#     @http.route('/coolteve_backend_style/coolteve_backend_style/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/coolteve_backend_style/coolteve_backend_style/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('coolteve_backend_style.listing', {
#             'root': '/coolteve_backend_style/coolteve_backend_style',
#             'objects': http.request.env['coolteve_backend_style.coolteve_backend_style'].search([]),
#         })

#     @http.route('/coolteve_backend_style/coolteve_backend_style/objects/<model("coolteve_backend_style.coolteve_backend_style"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('coolteve_backend_style.object', {
#             'object': obj
#         })