 # -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Devintelle Solutions (<http://devintellecs.com/>).
#
##############################################################################

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp

class AccountInvoiceLine(models.Model):
	_inherit = "account.invoice.line"

	total_vat = fields.Float("Amount Tax",compute='_get_invoice_line_tax')
	price_subtotal_with_vat = fields.Float("Subtotal with Tax",compute='_get_invoice_line_tax')
	
	@api.multi
	@api.one
	@api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id')
	def _get_invoice_line_tax(self):
		if self.invoice_line_tax_ids:
			currency = self.invoice_id and self.invoice_id.currency_id or None
			price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
			taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
			
			sum_taxes = []
		 	# Extracting tax amount for different types of taxes
			for counter in range(len(taxes['taxes'])):
				sum_taxes.append(taxes['taxes'][counter]['amount'])
			sum_taxes = sum(sum_taxes)
			
			self.total_vat = sum_taxes
			self.price_subtotal_with_vat = self.price_subtotal + sum_taxes
