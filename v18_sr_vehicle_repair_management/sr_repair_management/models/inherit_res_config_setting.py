# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    so_type = fields.Selection([('in_diagnosis', 'In Diagnosis'),('in_work_order', 'In Work Order')],
                               string="Sale Order Type",
                               default='in_diagnosis',
                               config_parameter='sr_repair_management.so_type')
