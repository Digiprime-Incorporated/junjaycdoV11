 # -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Devintelle Solutions (<http://devintellecs.com/>).
#
##############################################################################

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
		
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    total_vat = fields.Float("Amount Tax",compute='_get_sale_order_line_tax')
    
    @api.multi
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _get_sale_order_line_tax(self):	
    	for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_id)
            line.total_vat = line.price_tax
