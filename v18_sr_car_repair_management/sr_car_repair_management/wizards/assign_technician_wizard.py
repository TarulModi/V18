# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, api, _


class AssignTechnicianWizard(models.TransientModel):
    _name = "assign.technician.wizard"
    _description = "Assign Technician Wizard"

    user_id = fields.Many2one("res.users", string="Technician")

    def assign_technician(self):
        active_id = self.env['car.diagnosis'].browse(self._context.get('active_id'))
        if active_id:
            active_id.write({
                'user_id' : self.user_id.id,
                'state' : 'in_progress'
            })
            active_id.repair_id.state = 'in_progress'
