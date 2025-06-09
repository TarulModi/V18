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
from odoo.exceptions import ValidationError


class TermStructure(models.Model):
    _name = "term.structure"
    _inherit = ['mail.thread']
    _description = "Term Structure"
    _rec_name = "name"

    name = fields.Char(string="Name", tracking=True, translate=True)
    no_of_term = fields.Integer(string="No of Term", tracking=True, default="1")

    @api.constrains('no_of_term')
    def check_no_of_term(self):
        """
        Constraint to ensure the number of terms is greater than zero.
        Raises ValidationError if an invalid number is entered.
        """
        for record in self:
            if record.no_of_term <= 0:
                raise ValidationError(_("Enter proper no of terms!"))