# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from datetime import date
from odoo import fields, api, models, _
from odoo.exceptions import ValidationError


# sr Warranty Report Wizard class.
class srWarrantyReportWizard(models.TransientModel):
    _name = "sr.warranty.report.wizard"
    _description = "Warranty Report"

    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    state = fields.Selection(
        [("in_warranty", "In Warranty"), ("expired_warranty", "Expired Warranty")]
    )

    # Start date validation function
    @api.onchange("start_date")
    def _end_date_onchange(self):
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError(_("Please select the correct start date."))

    # End date validation function
    @api.onchange("end_date")
    def _start_date_onchange(self):
        if self.start_date and self.start_date > self.end_date:
            raise ValidationError(_("Please select the correct end date."))

    # Print pdf report function
    def print_pdf_report(self):
        data = {}
        return self.env.ref(
            "sr_warranty_management.sr_product_warranty_report_action"
        ).report_action(None, data=data)
