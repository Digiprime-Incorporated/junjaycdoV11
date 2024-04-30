# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, _
from datetime import datetime


class PR_Reject(models.Model):

    _name = 'skit.pr.reject.wizard'
    _description = "Product Refund"
    
    request_id = fields.Many2one('purchase.request',"Request")
    comment = fields.Text("Comments")
    approval_id =fields.Many2one('skit.request.approval')
    
    @api.multi
    def reject_approval(self):
        request_id = self.env.context['request_id']
        approval_id = self.env.context['approval_id']
        comments = self.comment
        request = self.env['purchase.request'].search([('id','=',request_id)])
        approval_request_id = self.env['skit.request.approval'].search([('request_id','=',request_id),
                                                                        ('id','=',approval_id)])
        if approval_request_id:
            approval_request_id.update({'status':'rejected',
                                        'sign_date':datetime.today(),
                                        'comment':comments})
        if request:
            request.update({'state':'rejected'})
    