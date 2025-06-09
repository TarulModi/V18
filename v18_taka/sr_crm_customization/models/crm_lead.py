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
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.constrains('stage_id')
    def _check_quotation_before_won(self):
        for lead in self:
            won_stage_ids = self.env['crm.stage'].search([('is_won', '=', True)]).ids
            if lead.stage_id.id in won_stage_ids and len(lead.order_ids.ids) < 1:
                raise UserError("You cannot move to 'Won' stage without a quotation being created.")