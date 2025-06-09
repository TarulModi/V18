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


class ClassStudent(models.Model):
    _name = "class.student"
    _inherit = ['mail.thread']
    _description = "Class Student"
    _rec_name = "student_id"

    class_room_id = fields.Many2one("class.room", string="Class Room", tracking=True)
    student_id = fields.Many2one("student.student", string="Student", tracking=True)
    roll_no = fields.Integer("Roll No.")
    name = fields.Char(related='student_id.name')