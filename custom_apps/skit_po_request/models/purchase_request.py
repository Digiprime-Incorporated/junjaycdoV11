# -*- coding: utf-8 -*-

from odoo import api, fields, models,_
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.exceptions import UserError
from werkzeug.urls import url_encode

_STATES = [
    ('draft', 'Draft'),
    ('to_approve', 'To be approved'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected')
]


class PurchaseRequest(models.Model):

    _name = 'purchase.request'
    _description = 'Purchase Request'
    # _inherit = ['mail.thread']

    @api.model
    def _company_get(self):
        company_id = self.env['res.company']._company_default_get(self._name)
        return self.env['res.company'].browse(company_id.id)

    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)

    @api.model
    def _get_default_name(self):
        return self.env['ir.sequence'].get('purchase.request')

    @api.model
    def _default_picking_type(self):
        type_obj = self.env['stock.picking.type']
        company_id = self.env.context.get('company_id') or \
            self.env.user.company_id.id
        types = type_obj.search([('code', '=', 'incoming'),
                                 ('warehouse_id.company_id', '=', company_id)])
        if not types:
            types = type_obj.search([('code', '=', 'incoming'),
                                     ('warehouse_id', '=', False)])
        return types[:1]

    @api.multi
    @api.depends('state')
    def _compute_is_editable(self):
        for rec in self:
            if rec.state in ('to_approve', 'approved', 'rejected'):
                rec.is_editable = False
            else:
                rec.is_editable = True

    @api.multi
    def _track_subtype(self, init_values):
        for rec in self:
            if 'state' in init_values and rec.state == 'to_approve':
                return 'skit_po_request.purchase_request_approve'
            elif 'state' in init_values and rec.state == 'approved':
                return 'skit_po_request.purchase_request_approved'
            elif 'state' in init_values and rec.state == 'rejected':
                return 'skit_po_request.purchase_request_rejected'
        return super(PurchaseRequest, self)._track_subtype(init_values)

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        self.ensure_one()
        default.update({
            'state': 'draft',
            'name': self.env['ir.sequence'].get('purchase.request'),
        })
        return super(PurchaseRequest, self).copy(default)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request') or 'New'
        request = super(PurchaseRequest, self).create(vals)
        #=======================================================================
        # if vals.get('assigned_to'):
        #     request.message_subscribe_users(user_ids=[request.assigned_to.id])
        #=======================================================================
        return request

    @api.multi
    def write(self, vals):
        res = super(PurchaseRequest, self).write(vals)
        #=======================================================================
        # for request in self:
        #     if vals.get('assigned_to'):
        #         self.message_subscribe_users(user_ids=[request.assigned_to.id])
        #=======================================================================
        return res

    @api.multi
    def button_draft(self):
        for rec in self:
            rec.state = 'draft'
            approve = self.env['skit.request.approval'].search([('request_id','=',rec.id)])
            for approve_id in approve:
                approve_id.unlink()
            self.partner_id = ""  
        return True
    
    def action_send_mail(self):
        self.ensure_one()
        user_id = self.partner_id
        template = self.env.ref('skit_po_request.po_request_approval_email_template', raise_if_not_found=False)
        mail_template = self.env['mail.template'].sudo().browse(template.id)
        mail_template.write({
                        'email_to': user_id.email
                    })
        mail_id = mail_template.send_mail(self.id, force_send=True)
        mail_mail_obj = self.env['mail.mail'].sudo().search(
                            [('id', '=', mail_id)]
                            )
        mail_mail_obj.send()
        mail_mail = self.env['mail.mail'].sudo().search(
                            [('id', '=', mail_mail_obj.id)]
                            )
    
    @api.multi
    def button_to_approve(self):
        approval_limit = 0
        user_id = self.env.uid
        approve = self.env['skit.request.approval']
        employee = self.env['hr.employee'].search([('user_id','=',user_id)],limit=1)
        ir_model = self.env['ir.model'].search([('model','=','purchase.request')],limit=1)
        sub_total = sum([line.price_subtotal for line in self.line_ids])
        job_id = self.env['hr.job'].search([('current_occupant_id','=',employee.id)],limit=1)
        approver_reached = False
        next_job = job_id
        job_approval_ids = self.env['skit.approval.limit'].search([('job_id','=',job_id.id),
                                                                 ('ir_model_id','=',ir_model.id)],limit=1)
        hr_job = self.env['hr.job'].search([('budget_override','=',True)],limit=1)
        if not job_id:
            approve.create({'request_id':self.id,
                                 'user_id':hr_job.current_occupant_id.user_id.id,
                                 'status':'pending_sign',
                                 'limit_amt':sub_total,
                                 })
            self.partner_id = hr_job.current_occupant_id.user_id.id
            for rec in self:
                rec.state = 'to_approve'
                return
        if job_id.budget_override:
            approve.create({'request_id':self.id,
                            'user_id':user_id,
                            'status':'signed',
                            'sign_date':datetime.today(),
                            })
            for rec in self:
                rec.state = 'approved'
                return
        for job in job_approval_ids:
            approval_limit = job.approval_limit
            approve.create({'request_id':self.id,
                                'user_id':user_id,
                                'status':'signed',
                                'sign_date':datetime.today(),
                                'limit_amt':approval_limit,
                                'delegate_user_id':next_job.delegate_user_id.id
                                })
            if approval_limit >= sub_total:              
                for rec in self:
                    rec.state = 'approved'
                    return
        while not approver_reached:
            next_job_id = next_job.report_next_job_id
            if not next_job_id:
                approve.create({'request_id':self.id,
                                 'user_id':hr_job.current_occupant_id.user_id.id,
                                 'status':'pending_sign',
                                 'limit_amt':sub_total,
                                 })
                for rec in self:
                    rec.state = 'to_approve'
                return
            limit_id = self.env['skit.approval.limit'].search([('job_id','=',next_job_id.id),
                                                                 ('ir_model_id','=',ir_model.id)],limit=1)
            if not self.partner_id:
                next_id =next_job_id.current_occupant_id.user_id
                self.partner_id = next_id.id
                if self.isemail:
                    if not next_id.login:
                        raise UserError(_("Cannot send email: user %s has no email address.") % next_id.name)
                    self.action_send_mail()
            if limit_id.approval_limit < sub_total:
                next_job = next_job_id
                if next_job.report_next_job_id:
                    next_user_id =next_job.report_next_job_id.current_occupant_id.user_id.id
                else:
                    next_user_id = hr_job.current_occupant_id.user_id.id
                    if next_job_id.budget_override:
                        approve.create({'request_id':self.id,
                                 'user_id':next_job_id.current_occupant_id.user_id.id,
                                 'status':'pending_sign',
                                 'limit_amt':sub_total,
                                 })
                        for rec in self:
                            rec.state = 'to_approve'
                        return
                approve.create({'request_id':self.id,
                                 'user_id':next_job_id.current_occupant_id.user_id.id,
                                 'status':'pending_sign',
                                 'next_user_id':next_user_id,
                                 'limit_amt':limit_id.approval_limit,
                                 'delegate_user_id':next_job_id.delegate_user_id.id
                                 })
            else:
                approve.create({'request_id':self.id,
                                 'user_id':next_job_id.current_occupant_id.user_id.id,
                                 'status':'pending_sign',
                                 'limit_amt':limit_id.approval_limit,
                                 'delegate_user_id':next_job_id.delegate_user_id.id
                                 })
                for rec in self:
                    rec.state = 'to_approve'
                approver_reached = True

        return True

    @api.multi
    def button_approved(self):
        user_id = self.env.uid
        delegate_user_id = False
        sub_total = sum([line.price_subtotal for line in self.line_ids])
        approval_id  = self.env['skit.request.approval'].search([('request_id','=',self.id),'|',
                                                        ('user_id','in',[user_id]),('delegate_user_id','=',user_id)
                                                        ])
        if approval_id:
            if approval_id.status =='signed':
                raise UserError(_('You have already signed this document.'))
            elif ((user_id != self.partner_id.id)
                  and (approval_id.user_id.id != self.partner_id.id)):
                raise UserError(_('You are not the next user in line to Approve.'))
            else:
                if user_id == approval_id.delegate_user_id.id:
                    employee = self.env['hr.employee'].search([('user_id','=',approval_id.delegate_user_id.id)])
                    if not employee.job_id:
                        raise UserError(_('This account has not been linked to a EmployeePostion.Please contact the Administrator.'))
                approval_id.update({'status':'signed',
                                    'sign_date':datetime.today()})
                self.update({'partner_id':approval_id.next_user_id.id})
                if self.isemail:
                    if not approval_id.next_user_id.login:
                        if approval_id.limit_amt < sub_total:
                            raise UserError(_("Cannot send email: user %s has no email address.") % approval_id.next_user_id.name)
                    self.action_send_mail()
                if approval_id.limit_amt >= sub_total:
                    for rec in self:
                        rec.state = 'approved'
        else:
            raise UserError(_('You are not an authorized user to validate.'))

        return True

    @api.multi
    def button_rejected(self):
        user_id = self.env.uid
        delegate_user_id = False
        approval_id  = self.env['skit.request.approval'].search([('request_id','=',self.id),'|',
                                                        ('user_id','in',[user_id]),('delegate_user_id','=',user_id)
                                                        ])
        if approval_id:
            if approval_id.status =='signed':
                raise UserError(_('You have already signed this document.'))
            elif ((user_id != self.partner_id.id)
                  and (approval_id.user_id.id != self.partner_id.id)):
                raise UserError(_('You are not the next user in line to Reject.'))
            else:
                if user_id == approval_id.delegate_user_id.id:
                    employee = self.env['hr.employee'].search([('user_id','=',approval_id.delegate_user_id.id)])
                    if not employee.job_id:
                        raise UserError(_('This account has not been linked to a EmployeePostion.Please contact the Administrator.'))
        else:
            raise UserError(_('You are not an authorized user to Reject.'))

        return {
                'name': _('Reject Approval'),
                'type': 'ir.actions.act_window',
                'res_model': 'skit.pr.reject.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('skit_po_request.pr_reject_form').ids,
                'target': 'new',
                'context': {
                    'request_id': self.id,
                    'approval_id':approval_id.id
                }
            }


    @api.multi
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.user.company_id.currency_id.compute(order.company_id.po_double_validation_amount, order.currency_id))\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
        return True

    name = fields.Char('Request Reference', size=32, required=True,
                       default='New',
                       track_visibility='onchange')
    origin = fields.Char('Source Document', size=32)
    date_start = fields.Date('Creation date',
                             help="Date when the user initiated the "
                                  "request.",
                             default=fields.Date.context_today,
                             track_visibility='onchange')
    requested_by = fields.Many2one('res.users',
                                   'Requested by',
                                   required=True,
                                   track_visibility='onchange',
                                   default=_get_default_requested_by)
    assigned_to = fields.Many2one('res.users', 'Approver',
                                  domain=lambda self: [("groups_id", "=", self.env.ref( "skit_po_request.group_purchase_request_manager").id)],
                                  track_visibility='onchange')
    description = fields.Text('Description')
    company_id = fields.Many2one('res.company', 'Company',
                                 required=True,
                                 default=_company_get,
                                 track_visibility='onchange')
    line_ids = fields.One2many('purchase.request.line', 'request_id',
                               'Products to Purchase',
                               readonly=False,
                               copy=True,
                               track_visibility='onchange')
    state = fields.Selection(selection=_STATES,
                             string='Status',
                             index=True,
                             track_visibility='onchange',
                             required=True,
                             copy=False,
                             default='draft')
    is_editable = fields.Boolean(string="Is editable",
                                 compute="_compute_is_editable",
                                 readonly=True)

    picking_type_id = fields.Many2one('stock.picking.type',
                                      'Picking Type', required=True,
                                      default=_default_picking_type)

    picking_id = fields.Many2one('stock.picking', 'Stock Picking')
    partner_id = fields.Many2one('res.users', 'Next User to Approve')
    isemail = fields.Boolean("Email Nodification", default=False)
    approval_ids = fields.One2many('skit.request.approval', 'request_id',
                               ' Request Approval')
    
    def get_full_url(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        u_params = {
                'id': self.id,
            'view_type': 'form',
            'model': 'purchase.request',
            'menu_id': self.env.ref('skit_po_request.menu_purchase_request').id,
            'action': self.env.ref('skit_po_request.purchase_request_form_action').id,
        }
        params = '/web?#%s' % url_encode(u_params)
        return base_url + params


class PurchaseRequestLine(models.Model):

    _name = "purchase.request.line"
    _description = "Purchase Request Line"
    # _inherit = ['mail.thread']

    @api.multi
    @api.depends('product_id', 'name', 'product_uom_id', 'product_qty',
                 'analytic_account_id', 'date_required', 'specifications')
    def _compute_is_editable(self):
        for rec in self:
            if rec.request_id.state in ('to_approve', 'approved', 'rejected'):
                rec.is_editable = False
            else:
                rec.is_editable = True

    @api.depends('product_id')
    def _compute_supplier_id(self):
        for rec in self:
            if rec.product_id:
                if rec.product_id.seller_ids:
                    rec.supplier_id = rec.product_id.seller_ids[0].name
                    
    @api.onchange('specifications')
    def onchange_specification(self):
        specification=''
        if self.specifications:
            specification = self.specifications
        if self.product_id:
            name = self.product_id.name
            self.name = name +' '+specification

    @api.onchange('product_id')
    def onchange_product_id(self):
        result = {}
        if not self.product_id:
            return result
        specification=''
        if self.specifications:
            specification = self.specifications
        if self.product_id:
            name = self.product_id.name
            if self.product_id.code:
                name = '[%s] %s' % (name, self.product_id.code)
            if self.product_id.description_purchase:
                name += '\n' + self.product_id.description_purchase
            if self.product_id.standard_price:
                self.price_unit = self.product_id.standard_price
            self.product_uom_id = self.product_id.uom_id.id
            result['domain'] = {'product_uom_id': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
            self.product_qty = 1
            self.name = name +' '+specification
        return result
            
    @api.onchange('product_uom_id')
    def onchange_product_uom_id(self):
        uom_id = self.product_uom_id
        self.update({'product_uom_id':uom_id})
        
    @api.depends('product_qty', 'price_unit')
    def _compute_amount(self):
        subtotal = 0
        for line in self:
            subtotal = (line.price_unit * line.product_qty)
            line.update({'price_subtotal': subtotal})
        
    
    product_id = fields.Many2one(
        'product.product', 'Product',
        domain=[('purchase_ok', '=', True)],
        track_visibility='onchange')
    name = fields.Char('Description', size=256,
                       track_visibility='onchange')
    product_uom_id = fields.Many2one('product.uom', 'Product Unit of Measure',
                                     track_visibility='onchange')
    product_qty = fields.Float('Quantity', track_visibility='onchange',
                               digits_compute=dp.get_precision(
                                   'Product Unit of Measure'))
    request_id = fields.Many2one('purchase.request',
                                 'Purchase Request',
                                 ondelete='cascade', readonly=True)
    company_id = fields.Many2one('res.company',
                                 related='request_id.company_id',
                                 string='Company',
                                 store=True, readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account',
                                          'Analytic Account',
                                          track_visibility='onchange')
    requested_by = fields.Many2one('res.users',
                                   related='request_id.requested_by',
                                   string='Requested by',
                                   store=True, readonly=True)
    assigned_to = fields.Many2one('res.users',
                                  related='request_id.assigned_to',
                                  string='Assigned to',
                                  store=True, readonly=True)
    date_start = fields.Date(related='request_id.date_start',
                             string='Request Date', readonly=True,
                             store=True)
    description = fields.Text(related='request_id.description',
                              string='Description', readonly=True,
                              store=True)
    origin = fields.Char(related='request_id.origin',
                         size=32, string='Source Document', readonly=True,
                         store=True)
    date_required = fields.Date(string='Request Date', required=True,
                                track_visibility='onchange',
                                default=fields.Date.context_today)
    is_editable = fields.Boolean(string='Is editable',
                                 compute="_compute_is_editable",
                                 readonly=True)
    specifications = fields.Text(string='Specifications')
    request_state = fields.Selection(string='Request state',
                                     readonly=True,
                                     related='request_id.state',
                                     selection=_STATES,
                                     store=True)
    supplier_id = fields.Many2one('res.partner',
                                  string='Preferred supplier',
                                  compute="_compute_supplier_id", store=True,
                                     readonly=False)

    procurement_id = fields.Many2one('procurement.order',
                                     'Procurement Order',
                                     readonly=True)
    purchase_id = fields.Many2one('purchase.order',
                                  "Purchase Order",
                                  readonly=True)
    purchase_line_id = fields.Many2one('purchase.order.line',
                                       "Purchase Order line",
                                       readonly=True)
    price_unit = fields.Float(string='Unit Price', digits=dp.get_precision('Product Price'))

    price_subtotal = fields.Float(compute='_compute_amount', string='Subtotal')
    
    
class Skit_Request_Approval(models.Model):
    _name = "skit.request.approval"
    
    request_id = fields.Many2one('purchase.request', 'Purchase Request')
    user_id = fields.Many2one('res.users', 'User')
    status = fields.Selection([
                                ('signed', _('Signed')),
                                ('pending_sign', _('Pending Signature')),
                                ('rejected', _('Rejected')),], string='Status')
    sign_date = fields.Date("Sign Date")
    comment = fields.Text("Comments")
    next_user_id = fields.Many2one('res.users', 'Next User')
    delegate_user_id = fields.Many2one('res.users', 'Delegate User')
    limit_amt = fields.Float(string='Amount', digits=dp.get_precision('Product Price'))
