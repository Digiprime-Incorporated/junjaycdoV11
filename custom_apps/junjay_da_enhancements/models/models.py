# -*- coding: utf-8 -*-

from odoo.addons import decimal_precision as dp
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    phone = fields.Char(related='partner_id.phone')
    mobile = fields.Char(related='partner_id.mobile')
    
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    total_vat = fields.Float(digits=dp.get_precision('Price Tax'), )
    price_subtotal = fields.Monetary(digits=dp.get_precision('Price Tax'), )
    price_total = fields.Monetary(digits=dp.get_precision('Price Total'), )
    
    