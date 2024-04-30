# -*- coding: utf-8 -*-
# Copyright (C) 2017-present  Technaureus Info Solutions(<http://technaureus.com/>)

from odoo import models, api
from odoo.tools.translate import _
# from odoo.tools import amount_to_text_en, float_round
# from odoo.tools.amount_to_text_en import amount_to_text


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.multi
    @api.depends('amount')
    def num_to_words(self, amount_total, cu_id):
        #take units of currency id
        m_unit = self.env['res.currency'].browse({cu_id.id}).currency_unit_label
        s_unit = self.env['res.currency'].browse({cu_id.id}).currency_sub_unit_label
        voucher_amount_in_words = amount_to_text_en.amount_to_text(self.amount, cu_id)

        if m_unit and s_unit:
            voucher_amount_in_words = voucher_amount_in_words.replace('euro', m_unit)
            voucher_amount_in_words = voucher_amount_in_words.replace('Cents', s_unit)
            voucher_amount_in_words = voucher_amount_in_words.replace('Cent', s_unit) 
            return voucher_amount_in_words
        
        elif m_unit and not s_unit:
            voucher_amount_in_words = voucher_amount_in_words.replace('euro', ' ')
            voucher_amount_in_words = voucher_amount_in_words.replace('Cents', m_unit)
            voucher_amount_in_words = voucher_amount_in_words.replace('Cent',  m_unit)
            return voucher_amount_in_words
        else:
            return voucher_amount_in_words