# -*- coding: utf-8 -*-

from openerp import fields, models, api
from openerp.exceptions import UserError, RedirectWarning, ValidationError

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.multi
    def post(self):
        res = super(AccountPayment, self).post()#calling super!
        #print self._context,"!!!!!!"
        flag = False
        if self._context.get('active_model') == 'account.invoice':
            invoice_id = self._context.get('active_id')
            invoice = self.env['account.invoice'].browse(invoice_id)
            flag = True

        for rec in self:
            if rec.apply_cash_register and rec.cash_register_id:
                if rec.partner_type == 'supplier':
                    amount = rec.amount * -1
                else:
                    amount = rec.amount * 1
                
                if flag:
                    if invoice.amount_total_signed < 0.0 and rec.partner_type == 'customer':
                        #print stop #amount_total_signed
                        amount = rec.amount * -1
                    if invoice.amount_total_signed < 0.0 and rec.partner_type == 'supplier':
                        amount = rec.amount * 1

                if not rec.communication:
                    name = rec.name
                else:
                    name = rec.communication
                    
                vals = {
                        'statement_id': rec.cash_register_id.id,
                        'date': rec.payment_date,
                        'ref': rec.name,
                        'partner_id': rec.partner_id.id,
                        'name': name,
                        'amount': amount,
                        }
                if self.journal_id != rec.cash_register_id.journal_id:
                    raise UserError("Payment method on payment is not match with method on cash register.")
                self.env['account.bank.statement.line'].create(vals)
        return res

    apply_cash_register = fields.Boolean(string="Add Cash Register Entry", default=False)
    cash_register_id = fields.Many2one('account.bank.statement' ,string="Cash Register", required=False)

