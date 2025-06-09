# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################
from odoo import fields, api, models, _


class Partner(models.Model):
    _inherit = 'res.partner'

    partner_type = fields.Selection([
        ('garage', 'Garage'),
        ('supplier', 'Supplier')
    ], "Partner Type")
    aadhar_no = fields.Char('Aadhar No.')
    ownership_type = fields.Selection([
        ('partnership', 'Partnership'),
        ('sole_proprietorship', 'Sole Proprietorship'),
        ('limited_liability_partnership', 'Limited Liability Partnership'),
        ('private_limited_company', 'Private Limited Company'),
        ('one_person_company', 'One Person Company'),
    ], "Ownership Type")
    owner_company_type = fields.Selection([
        ('private_limited_company', 'Private Limited Company'),
        ('public_limited_company', 'Public Limited Company'),
        ('one_person_company', 'One Person Company'),
        ('limited_liability_partnership', 'Limited Liability Partnership'),
        ('section_8_company', 'Section 8 Company'),
    ], "Owner Company Type")
    kam_user_id = fields.Many2one('res.users', "KAM User")
    manpower = fields.Integer('Manpower')
    area = fields.Float('Area')
    uom_id = fields.Many2one('uom.uom', 'UOM')
    lat = fields.Char("Lat")
    long = fields.Char("Long")
    verification_status = fields.Selection([
        ('created', 'Created'),
        ('lat_long_varified', 'Bank Details and Lat long verified'),
        ('onboarded', 'On-boarded'),
        ('active', 'Active'),
    ], "Verification Status")
    verification_date = fields.Date('Verification Date', default=fields.Date.context_today)
    cluster_id = fields.Many2one('partner.cluster', "Cluster")
    cluster_name = fields.Char(related='cluster_id.name', string='Cluster Name')
    location_id = fields.Many2one('stock.location', 'Location')

    @api.onchange('verification_status')
    def _onchange_verification_status(self):
        self.verification_date = fields.Date.today()
