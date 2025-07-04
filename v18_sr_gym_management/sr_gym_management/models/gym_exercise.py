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


class gymExercise(models.Model):
    _name = "gym.exercise"
    _inherit = ['mail.thread']
    _description = "GYM Exercise"
    _rec_name = "name"

    name = fields.Char(string="Exercise Name", tracking=True, translate=True)
    exercise_for_ids = fields.Many2many("exercise.for", string="Exercise For", tracking=True)
    product_template_ids = fields.Many2many("product.template", string="Equipments",
                                            domain="[('is_equipment' , '=', True)]", tracking=True)
    time = fields.Integer("Time", tracking=True)
    calories_burn = fields.Integer("Calories Burn", tracking=True)
    benefits = fields.Html("Benefits", tracking=True)
    steps = fields.Html("Steps", tracking=True)


    def copy_data(self, default=None):
        vals_list = []
        default = default or {}
        for record in self:
            new_name = f"{record.name} (copy)"
            new_default = default.copy()
            new_default.update({'name': new_name})
            copied_vals = super(gymExercise, record).copy_data(default=new_default)
            vals_list.extend(copied_vals)
        return vals_list