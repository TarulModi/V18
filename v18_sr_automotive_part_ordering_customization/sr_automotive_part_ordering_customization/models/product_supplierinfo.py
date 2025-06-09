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


class ProductSupplier(models.Model):
    _inherit = 'product.supplierinfo'

    priority = fields.Integer('Priority')
    brand_id = fields.Many2one('product.brand', "Brand")
    ap = fields.Integer("AP")
    gp = fields.Integer("GP")
    cluster_id = fields.Many2one('partner.cluster')
    cluster_name = fields.Char(related='cluster_id.name', string='Cluster Name')
