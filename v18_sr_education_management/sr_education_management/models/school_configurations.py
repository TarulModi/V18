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


class SchoolConfigurations(models.Model):
    _name = "school.configurations"
    _inherit = ['mail.thread']
    _description = "School Configurations"
    _rec_name = "name"

    name = fields.Char(string="Name", tracking=True, translate=True)
    code = fields.Char(string="Code", tracking=True, translate=True)
    street = fields.Char('Street', readonly=False, store=True, tracking=True, translate=True)
    street2 = fields.Char('Street2', readonly=False, store=True, tracking=True, translate=True)
    zip = fields.Char('Zip', change_default=True, readonly=False, store=True, tracking=True, translate=True)
    city = fields.Char('City', readonly=False, store=True, tracking=True, translate=True)
    state_id = fields.Many2one("res.country.state", string='State', readonly=False, store=True,
        domain="[('country_id', '=?', country_id)]", tracking=True)
    country_id = fields.Many2one('res.country', string='Country', readonly=False, store=True, tracking=True)
    currency_id = fields.Many2one("res.currency", string='Currency', tracking=True)
    language_id = fields.Many2one("language.language", string='Language', tracking=True)