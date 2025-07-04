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


class hrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_trainer = fields.Boolean(string='GYM Trainer', tracking=True)
    trainer_skills_ids = fields.Many2many("trainer.skills", string="Specialization", tracking=True)
    trainer_type = fields.Selection([('personal', 'Personal'), ('general', 'General')], default='general')
