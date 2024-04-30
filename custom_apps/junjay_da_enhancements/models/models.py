# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    phone = fields.Char(related='partner_id.phone')
    mobile = fields.Char(related='partner_id.mobile')