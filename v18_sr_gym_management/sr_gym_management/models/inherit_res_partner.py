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


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_gym_member = fields.Boolean(string='GYM Member', tracking=True)
    employee_id = fields.Many2one("hr.employee", string="Trainer", tracking=True, domain="[('is_trainer', '=', True)]")
    trainer_skills_ids = fields.Many2many(related="employee_id.trainer_skills_ids", tracking=True)
    membership_ids = fields.One2many("gym.member.membership", 'partner_id', string="Membership", tracking=True)


    def button_buy_membership(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Buy Membership'),
            'res_model': 'buy.membership.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_partner_id': self.id,
            }
        }