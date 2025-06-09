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
from odoo.exceptions import UserError, ValidationError


class AssignTechnicianWizard(models.TransientModel):
    _name = "assign.technician.wizard"
    _description = "Assign Technician Wizard"

    user_id = fields.Many2one("res.users", string="Technician")
    line_ids = fields.One2many('assign.technician.wizard.line', 'wizard_id')

    @api.model
    def default_get(self, fields):
        res = super(AssignTechnicianWizard, self).default_get(fields)
        workorder_list = []
        active_id = self.env['repair.diagnosis'].browse(self._context.get('active_id'))
        if active_id and active_id.checklist_ids:
            for workorder in active_id.checklist_ids:
                if workorder:
                    workorder_list.append((0, 0, {
                        'checklist_id': workorder.id,
                    }))
        res.update({'line_ids': workorder_list})
        return res

    def assign_technician(self):
        if any(not cl.user_id for cl in self.line_ids):
            raise ValidationError("Please assign a technician to all checklist lines before proceeding.")

        active_id = self.env['repair.diagnosis'].browse(self._context.get('active_id'))
        if active_id:
            for line in self.line_ids:
                if line.checklist_id:
                    line.checklist_id.user_id = line.user_id.id
            active_id.create_work_order_records()


class AssignTechnicianWizardLine(models.TransientModel):
    _name = "assign.technician.wizard.line"
    _description = "Assign Technician Wizard Line"

    wizard_id = fields.Many2one("assign.technician.wizard")
    user_id = fields.Many2one("res.users", string="Technician", required=True)
    checklist_id = fields.Many2one('repair.checklist', string='CheckList', readonly=True, store=True)
