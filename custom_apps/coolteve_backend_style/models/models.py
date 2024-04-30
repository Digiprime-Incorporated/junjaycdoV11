# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class coolteve_backend_style(models.Model):
#     _name = 'coolteve_backend_style.coolteve_backend_style'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100