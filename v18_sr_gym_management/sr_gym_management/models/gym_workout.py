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


class gymWorkout(models.Model):
    _name = "gym.workout"
    _inherit = ['mail.thread']
    _description = "GYM Workout"
    _rec_name = "name"

    name = fields.Char(string="Workout Name", tracking=True, translate=True)
    employee_id = fields.Many2one("hr.employee", string="Trainer", domain="[('is_trainer' , '=', True)]", tracking=True)
    calories_burn = fields.Integer("Calories Burn", tracking=True)
    product_template_ids = fields.Many2many("workout.days", string="Workout Days", tracking=True)
    workout_exercise_ids = fields.One2many("gym.workout.exercise", 'workout_id', tracking=True)


    def copy_data(self, default=None):
        vals_list = []
        default = default or {}
        for record in self:
            new_name = f"{record.name} (copy)"
            new_default = default.copy()
            new_default.update({'name': new_name})
            copied_vals = super(gymWorkout, record).copy_data(default=new_default)
            vals_list.extend(copied_vals)
        return vals_list