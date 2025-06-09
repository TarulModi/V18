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


class HospitalEmployee(models.Model):
    _inherit = 'hr.employee'

    is_doctor = fields.Boolean(string="Is a Doctor", tracking=True)
    is_staff = fields.Boolean(string="Is a Staff Member", tracking=True)

    doctor_specialization = fields.Many2one('hospital.specialization', string="Specialization",
                                            domain="[('is_medical', '=', True)]", tracking=True)
    available_slots = fields.Text(string="Available Time Slots", tracking=True)
    qualification = fields.Char(string="Qualification", tracking=True)
    total_year_exp = fields.Float(string="Total Years of Experience", tracking=True)
    age = fields.Float(string="Age", tracking=True)

    @api.model
    def create(self, vals):
        employee = super(HospitalEmployee, self).create(vals)
        if employee.is_doctor and employee.department_id:
            employee.department_id.write({
                'doctor_ids': [(4, employee.id)]
            })
        return employee

    def write(self, vals):
        res = super(HospitalEmployee, self).write(vals)
        if 'department_id' in vals:
            for employee in self:
                if employee.is_doctor and employee.department_id:
                    employee.department_id.write({
                        'doctor_ids': [(4, employee.id)]
                    })
                if not employee.department_id:
                    if employee.is_doctor:
                        old_department = self.env['hr.department'].search([('doctor_ids', 'in', employee.id)])
                        if old_department:
                            old_department.write({
                                'doctor_ids': [(3, employee.id)]
                            })
        return res
