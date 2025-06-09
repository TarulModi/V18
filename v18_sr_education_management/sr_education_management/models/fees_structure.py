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
from odoo.exceptions import ValidationError


class FeesStructure(models.Model):
    """
        This model defines the structure of academic fees associated
        with specific courses, academic years, and terms.

        Features:
        - Academic term-wise fees setup
        - Integration with academic year and course configuration
        - Auto computation of fees per term
        - Messaging & tracking enabled for changes (via mail.thread)
        """
    _name = "fees.structure"
    _inherit = ['mail.thread']
    _description = "Fees Structure"

    name = fields.Char("Name", tracking=True)
    academic_year_id = fields.Many2one("academic.year", string="Academic Year", tracking=True)
    term_ids = fields.Many2many("academic.terms", string="Academic Terms")
    course_id = fields.Many2one("courses.courses", string="Course", tracking=True)
    fees_per_term = fields.Float("Fees per Term", compute="_compute_fees_amount")
    line_ids = fields.One2many("fees.structure.line", "fees_structure_id", string="Fees Structure Lines")

    @api.depends('line_ids.amount')
    def _compute_fees_amount(self):
        """
        Computes the total fees from all associated line items.
        """
        for rec in self:
            rec.fees_per_term = sum(rec.line_ids.mapped('amount'))

class FeesStructureLine(models.Model):
    """
       This model defines individual line items for a Fees Structure.
       Each line represents a fee component (e.g., Tuition, Lab, Transport),
       linked to a product and associated with an overall fees.structure.
       """
    _name = "fees.structure.line"
    _description = "Fees Structure Lines"

    fees_structure_id = fields.Many2one("fees.structure")
    product_id = fields.Many2one("product.product", string="Fees Type")
    amount = fields.Float("Amount")

    @api.onchange("product_id")
    def _onchange_product(self):
        """
        Auto-update the amount field based on the selected product's standard price.
        Ensures that fee amounts are pre-filled according to predefined prices.
        """
        for rec in self:
            if rec.product_id:
                rec.amount = rec.product_id.standard_price
            else:
                rec.amount = 0.0