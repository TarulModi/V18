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


class gymWorkoutExercise(models.Model):
    _name = "gym.workout.exercise"
    _inherit = ['mail.thread']
    _description = "GYM Work Exercise"
    _rec_name = "exercise_id"

    workout_id = fields.Many2one("gym.workout")
    exercise_id = fields.Many2one("gym.exercise")
    exercise_for_ids = fields.Many2many(related="exercise_id.exercise_for_ids", tracking=True)
    product_template_ids = fields.Many2many(related="exercise_id.product_template_ids", tracking=True)
    sets = fields.Integer("Sets", tracking=True)
    repeat = fields.Integer("Repeat", tracking=True)
    weight = fields.Float("Weight", tracking=True)
