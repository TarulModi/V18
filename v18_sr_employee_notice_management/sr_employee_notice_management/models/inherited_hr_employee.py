# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def count_notice(self):
        for emp in self:
            emp.notice_count = len(self.env['sr.grant.employee.notice'].search([('employee_id','=', emp.id)]))

    def action_view_notice(self):
        notice = self.env['sr.grant.employee.notice'].search([('employee_id','=', self.id)])
        action = self.env.ref('sr_employee_notice_management.sr_grant_notice_action').read()[0]
        if len(notice) > 1:
            action['domain'] = [('id', 'in', notice.ids)]
        elif len(notice) == 1:
            form_view = [(self.env.ref('sr_employee_notice_management.sr_hr_employee_grant_notice_form_view').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = notice.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        return action

    notice_count = fields.Integer('# Notice Granted', compute="count_notice")