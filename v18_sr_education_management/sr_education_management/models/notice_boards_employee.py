# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import api, fields, models, _


class NoticeBoardsEmployee(models.Model):
    _name = "notice.boards.employee"
    _inherit = ['mail.thread']
    _description = "Notice Boards Employee"
    _rec_name = "employee_id"

    notice_boards_id = fields.Many2one("notice.boards", string="Notice Boards", tracking=True)
    employee_id = fields.Many2one("hr.employee", string="Employee", tracking=True, domain=[('is_faculty', '=', True)])
