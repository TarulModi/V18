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


class BmiCalculation(models.Model):
    _name = "bmi.calculation"
    _inherit = ['mail.thread']
    _description = "BMI Calculation"
    _rec_name = "member_id"

    def _get_default_weight_uom(self):
        return self.env['product.template']._get_weight_uom_name_from_ir_config_parameter()

    member_id = fields.Many2one('res.partner', string='Member',tracking=True, required=True,
                                domain="[('is_gym_member', '!=',False)]")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Gender", required=True, tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    date = fields.Date(string='Date', tracking=True)
    height = fields.Float('Height', tracking=True)
    height_uom_name = fields.Char(string='Height unit of measure label', default='cm', tracking=True)
    weight = fields.Float('Weight', tracking=True)
    weight_uom_name = fields.Char(string='Weight unit of measure label',default=_get_default_weight_uom,tracking=True)
    bmi = fields.Float(string='BMI', store=True, compute='_compute_bmi_bmr', tracking=True)
    bmr = fields.Float(string='BMR', store=True, compute='_compute_bmi_bmr', tracking=True)

    @api.depends('weight', 'height', 'gender', 'age')
    def _compute_bmi_bmr(self):
        self.bmi = self.bmr = 0
        if self.weight and self.height:
            self.bmi = (self.weight / self.height / self.height) * 10000
            if self.gender == "male":
                self.bmr = 66.47 + (13.75 * self.weight) + \
                           (5.003 * self.height) - (6.755 * self.age)
            if self.gender == "female":
                self.bmr = 655.1 + (9.563 * self.weight) + \
                           (1.85 * self.height) - (6.755 * self.age)
        else:
            self.bmi = 1
            self.bmr = 1