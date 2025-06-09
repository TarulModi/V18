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


class Religions(models.Model):
    _name = "religions.religions"
    _inherit = ['mail.thread']
    _description = "Religions"
    _rec_name = "name"

    name = fields.Char(string="Name", tracking=True, translate=True)