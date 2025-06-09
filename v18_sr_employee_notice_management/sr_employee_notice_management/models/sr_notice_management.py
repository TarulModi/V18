# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, api, _


class srEmployeeGrantNotice(models.Model):
    _name = 'sr.grant.employee.notice'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Employee Offense Notice'

    name = fields.Char('Name', default=lambda self: _('New'), index=True, copy=False)
    employee_id = fields.Many2one('hr.employee', 'Employee', index=True, required=True)
    manager_id = fields.Many2one('hr.employee', 'Manager', index=True)
    department_id = fields.Many2one('hr.department', 'Department', index=True, required=True)
    user_id = fields.Many2one('res.users', string='User',
                              default=lambda self: self.env.uid, required=True)
    job_title = fields.Char('Job Title')
    identification_no = fields.Char('Identification No')
    company_id = fields.Many2one('res.company', string='Company', 
                                 index=True,
                                 default=lambda self: self.env.user.company_id)
    offense_id = fields.Many2one('sr.employee.offense', string='Offense')
    warning = fields.Selection([('first','First Warning'),
                                     ('second','Second Warning'),
                                     ('final','Final Warning')], 'Warning')
    
    date = fields.Date("Date", index=True, readonly=True, default=fields.Date.context_today)
    offense_decision = fields.Text('Decision of Offense')
    offense_improvement = fields.Text('Action Improvement')
    overcome_offense = fields.Text('Future offense warning')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel','Cancel'),
        ], string='State', default="draft", index=True, tracking=True, copy=False)
    comment = fields.Text('Comments')

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        values = {
            'manager_id': self.employee_id.parent_id and self.employee_id.parent_id.id,
            'identification_no': self.employee_id.identification_id and self.employee_id.identification_id,
            'department_id': self.employee_id.department_id and self.employee_id.department_id.id,
            'job_title': self.employee_id.job_title and self.employee_id.job_title,
        }
        self.update(values)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('sr.sequence.notice') or _('New')
        return super(srEmployeeGrantNotice, self).create(vals_list)

    def confirm_notice(self):
        self.state = 'confirm'

    def notice_done(self):
        self.state = 'done'

    def notice_cancel(self):
        self.state = 'cancel'

    def draft_notice(self):
        self.state = 'draft'


class srEmployeeOffense(models.Model):
    _name = 'sr.employee.offense'
    _description = 'Offense for the employee'

    name = fields.Char('Name', required=True)
