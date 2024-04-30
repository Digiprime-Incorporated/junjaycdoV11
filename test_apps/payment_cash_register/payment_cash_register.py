# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import Warning


class cash_statement(models.Model):
    _inherit = 'account.bank.statement'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        if view_type == 'form' and self._context.get('voucher_pay_id', False):
            result = self.env.ref('account.view_bank_statement_form2')
            view_id = result.id or False
        res = super(cash_statement, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=False)
        return res


class account_bank_statement_line(models.Model):
    _inherit = 'account.bank.statement.line'
    _description = 'St Line'

    voucher_pay_id = fields.Many2one('account.voucher', string='Account Voucher')


class account_voucher(models.Model):
    _inherit = 'account.voucher'
    _description = 'Account Voucher'

    update_cash = fields.Boolean(
        string='Update Cash Register?',
        readonly=True,
        states={'draft':[('readonly', False)]},
        help='Tick if you want to update cash register by creating cash transaction line.',
    )
    cash_id = fields.Many2one(
        'account.bank.statement',
        string='Cash Register',
        domain=[('journal_id.type', 'in', ['cash']),
                ('state', '=', 'open')],
        readonly=True,
        states={'draft':[('readonly', False)]}
    )

    @api.model 
    def voucher_move_line_create(self, voucher_id, line_total,
                                 move_id, company_currency, current_currency):
        line_obj = self.env['account.move.line']
        statement_line_obj = self.env['account.bank.statement.line']
        voucher_obj = self.env['account.voucher']
        res =\
            super(account_voucher, self).voucher_move_line_create(voucher_id, line_total,
                                                                  move_id, company_currency,
                                                                  current_currency)
        voucher = voucher_obj.browse(voucher_id)
        current_currency_obj = voucher.currency_id or\
            voucher.journal_id.company_id.currency_id
        ctx = dict(self._context.copy())
        ctx.update({'date': voucher.date})
        if res:
            if voucher.update_cash:
                for r1 in res[1]:
                    for r in line_obj.browse(r1):  # super returns two ids in r1 one is for sale entry and one for cash to reconcile..so we take first which is relatedto cash
                        if not voucher.name and not voucher.reference:
                            raise Warning(_('Error !'), _('Please provide payment referene or Memo on payment'))
                        if r.account_id.type == 'payable':
                            company_currency_id = self._get_company_currency(voucher.id)
                            company_currency = self.env['res.currency'].browse(company_currency_id)
                            amount_convert = company_currency.with_context(ctx).compute(r.debit, current_currency_obj)
                            statement_line_obj.create({
                                'name': voucher.name or voucher.reference or voucher.number or voucher.id,
                                'amount':-amount_convert,  # -r.debit
                                'type': 'supplier',
                                'partner_id': r.partner_id.id,
                                'account_id': r.account_id.id,
                                'statement_id': voucher.cash_id.id,
                                'ref': voucher.number or voucher.reference or voucher.id,
                                'date': r.date,
                                'voucher_pay_id':voucher.id,
                            })
                            #r.write({'statement_id': voucher.cash_id.id})  # link journal itmesn with cash register
                            self._cr.execute('update account_move_line set statement_id=%s where id=%s', (voucher.cash_id.id, r.id))
                            break
                        if r.account_id.type == 'receivable':
                            company_currency_id = self._get_company_currency(voucher.id)
                            company_currency = self.env['res.currency'].browse(company_currency_id)
                            amount_convert = company_currency.with_context(ctx).compute(r.credit, current_currency_obj)
                            statement_line_obj.create({
                                'name': voucher.name or voucher.reference or voucher.number or voucher.id,
                                'amount': amount_convert,  # r.credit
                                'type': 'customer',
                                'partner_id': r.partner_id.id,
                                'account_id': r.account_id.id,
                                'statement_id': voucher.cash_id.id,
                                'ref': voucher.number or voucher.reference or voucher.id,
                                'date': r.date,
                                'voucher_pay_id':voucher.id,
                            })
#                            r.write({'statement_id': voucher.cash_id.id})#probuse todo uncomment.
                            break
        return res

    @api.one
    @api.constrains('journal_id')
    def _check_destination_jrnl(self):
        if self.update_cash and self.journal_id.type == 'bank':
            raise Warning('You can not update cash register if the journal is of type bank.') 
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
