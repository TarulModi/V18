# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, models


class srReportTemplateConfiguration(models.Model):
    _name = 'sr.report.template.configuration'
    _description = "Report Template Configuration"
    
    name = fields.Char(string="Name", required=True)
    is_show_company = fields.Boolean(string="Company Details in Report")
    is_print_total = fields.Boolean(string="Total in Report")
    excel_sheet_name = fields.Char(string="Excel Sheet Name", required=True)
    header_title = fields.Char(string="Header Name", required=True)
    
    #Company Details
    company_font_name = fields.Char(string="Font Name")
    company_font_size = fields.Char(string="Font Size")
    company_font_color = fields.Char(string="Font Color")
    company_background_color = fields.Char(string="Background Color")
    is_company_bold = fields.Boolean(string="Bold")
    is_company_italic = fields.Boolean(string="Italic")
    
    #Total Details
    total_background_color = fields.Char(string="Background Color")
    total_Font_color = fields.Char(string="Font Color")
    
    #Header Details
    header_font_name = fields.Char(string="Font name")
    header_font_size = fields.Char(string="Font Size")
    header_font_color = fields.Char(string="Font Color")
    header_background_color = fields.Char(string="Background Color")
    is_header_bold = fields.Boolean(string="Bold")
    is_header_italic = fields.Boolean(string="Italic")
