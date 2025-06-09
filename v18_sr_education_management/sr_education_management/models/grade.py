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


class Grade(models.Model):
    _name = "grade.grade"
    _inherit = ['mail.thread']
    _description = "Grade"
    _rec_name = "name"

    name = fields.Char(string="Name", tracking=True, translate=True)
    gpa = fields.Float(string="GPA", tracking=True)
    min_per = fields.Float(string="Minimum Percentage", tracking=True)
    max_per = fields.Float(string="Maximum Percentage", tracking=True)
