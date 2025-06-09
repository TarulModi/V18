# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, api
from odoo import _
from odoo.exceptions import ValidationError


class srExpenceLimit(models.Model):
    _name = "expence.expence"

    emp_id = fields.Many2one('hr.employee')
    expence_limit = fields.Integer("Expence Limit")
    product_id = fields.Many2one('product.product')


class srExpencEmpLimit(models.Model):
    _inherit = "hr.employee"

    expence = fields.One2many('expence.expence', 'emp_id', 'Products')

class srExpenceLimitPro(models.Model):
    _inherit = "product.template"

    expence_limit = fields.Float("Expence Limit")

class srHrExpence(models.Model):
    _inherit = "hr.expense"

    @api.constrains("product_id", "price_unit", "employee_id", "employee_id.expence.product_id", "product_id.expence_limit", "employee_id.expence_limit")
    def expence_limit(self):
        rec = self.employee_id.expence.filtered(lambda x:x.product_id == self.product_id)
        if rec:
            if self.price_unit > rec.expence_limit:
                msg = ("Your " + str(self.product_id.name) + " Expense is more than Expense limit "+ str(rec.expence_limit))
                raise ValidationError(msg)
        elif not rec:
            if self.product_id.expence_limit < self.price_unit:
                msg = ("Your Expense " + str(self.product_id.name) + " Expense is more than Expense limit " + str(self.product_id.expence_limit))
                raise ValidationError(msg)
