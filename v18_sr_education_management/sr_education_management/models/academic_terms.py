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


class AcademicTerms(models.Model):
    _name = "academic.terms"
    _inherit = ['mail.thread']
    _description = "Academic Terms"
    _rec_name = "name"

    academic_year_id = fields.Many2one("academic.year", string="Academic Year", tracking=True)
    sequence = fields.Integer("Sequence")
    name = fields.Char(string="Name", tracking=True, translate=True)
    start_date = fields.Date(string="Start Date", tracking=True)
    end_date = fields.Date(string="End Date", tracking=True)
    parent_id = fields.Many2one("academic.year", string="Parent Term", tracking=True)
