 # -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Devintelle Solutions (<http://devintellecs.com/>).
#
##############################################################################

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
		
class tax_purchase_line(models.Model):
    _inherit = "purchase.order.line"

    total_vat = fields.Float("Amount Tax",compute='_get_purchase_order_line_tax')
    price_subtotal_with_vat = fields.Float("Subtotal with Tax",compute='_get_purchase_order_line_tax')
    
    @api.multi
    @api.depends('product_qty', 'price_unit', 'taxes_id')
    def _get_purchase_order_line_tax(self):	
    	for line in self:
    		taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_qty, product=line.product_id, partner=line.order_id.partner_id)
    		line.total_vat = line.price_tax
    		line.price_subtotal_with_vat = line.price_subtotal + line.price_tax
