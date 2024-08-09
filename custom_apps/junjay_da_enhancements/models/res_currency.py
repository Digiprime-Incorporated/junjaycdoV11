# -*- coding: utf-8 -*-

from odoo.addons import decimal_precision as dp
from odoo import models, fields, api

class ResCurrency(models.Model):
    _inherit = 'res.currency'
    
    decimal_places = fields.Integer()
    
    @api.multi
    @api.depends('rounding')
    def _compute_decimal_places(self):
        self.decimal_places = 2
        # for currency in self:
        #     if 0 < currency.rounding < 1:
        #         currency.decimal_places = int(math.ceil(math.log10(1/currency.rounding)))
        #     else:
        #         currency.decimal_places = 0
          