# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Skit_hr_employee(models.Model):
    _inherit = 'hr.employee'
    
    report_next_job_id = fields.Many2one('hr.job', 'Reports To Next Job')
    
    @api.onchange('job_id')
    def onchange_job_title(self):
        if self.job_id:
            report_next_job = self.job_id.report_next_job_id
            if report_next_job:
                self.update({'report_next_job_id':report_next_job.id})
            else:
                self.report_next_job_id = False
                
    
class Skit_HR_Job(models.Model):
    _inherit = "hr.job"
    
    report_next_job_id = fields.Many2one('hr.job', 'Reports To Next Job')
    current_occupant_id = fields.Many2one('hr.employee', string="Current Occupant",
                                        )
    budget_override = fields.Boolean('Budget Override', default=False)
    delegate_user_id = fields.Many2one('res.users', string="Delegate User")
    approval_limit_ids = fields.One2many('skit.approval.limit', 'job_id',
                                       string="Approval Limit")
    current_occ_id = fields.Many2one('hr.employee', string="Current Occupant",compute='_compute_current_occupant')
    
    
    @api.depends('current_occ_id')
    def _compute_current_occupant(self):
        for job in self:
            employee = self.env['hr.employee'].search([('job_id','=',job.id)], limit=1)
            job.write({'current_occupant_id':employee.id})
            job.current_occ_id = employee.id
    
class Skit_Approval_limit(models.Model):
    _name = "skit.approval.limit"
    
    job_id = fields.Many2one('hr.job', 'Job')
    ir_model_id = fields.Many2one('ir.model', 'Odoo Model' ,domain=[('model', '=', ('purchase.request'))])
    approval_limit = fields.Float("Approval Limit")
    increase_limit = fields.Float("Increase Limit")
