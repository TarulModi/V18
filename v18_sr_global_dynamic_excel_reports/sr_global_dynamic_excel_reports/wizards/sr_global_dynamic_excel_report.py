# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

import io
import pytz
import xlwt
import base64
import itertools, operator
from datetime import datetime
from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class srGlobalExcelReportWizard(models.TransientModel):
    _name = 'sr.global.excel.report.wizard'
    _description = "Global Excel Report Wizard"
    
    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')
    name = fields.Char('filename', readonly=True)
    data = fields.Binary('file', readonly=True)
    sheet_per_record = fields.Boolean('Sheet Per Record?')

    def _insert_company_detail(self, row, col, worksheet, global_dynamic_report_id):
        font_color = global_dynamic_report_id.template_id.company_font_color or 'black'
        font_name = global_dynamic_report_id.template_id.company_font_name or 'Times New Roman'
        font_size = global_dynamic_report_id.template_id.company_font_size or '200'
        background_color = global_dynamic_report_id.template_id.company_background_color or 'white'
        if global_dynamic_report_id.template_id.is_company_italic:
            is_italic = 'on'
        else:
            is_italic = 'off'
        if global_dynamic_report_id.template_id.is_company_bold:
            is_bold = 'on'
        else:
            is_bold = 'off'
        
        style_company_details = xlwt.easyxf("font: color " + font_color + 
                    "; font: name " + font_name + 
                    "; font:height " + font_size + 
                    "; font: italic " + is_italic + 
                    "; font: bold " + is_bold + 
                    "; align: vert centre, horiz centre; pattern: pattern solid, pattern_fore_colour " + background_color 
                    )
        user_id = self.env['res.users'].browse(self._uid)
        company_address = user_id.company_id.name + "\n"
        if user_id.company_id.street:
            company_address += user_id.company_id.street + "\n"
        if user_id.company_id.street2:
            company_address += user_id.company_id.street2 + "\n"
        if user_id.company_id.city:
            company_address += user_id.company_id.city + "\n"
        if user_id.company_id.state_id:
            company_address += user_id.company_id.state_id.name + "\n"
        if user_id.company_id.country_id:
            company_address += user_id.company_id.country_id.name 
        worksheet.write_merge(3, 12, 0, (len(global_dynamic_report_id.parent_object_field_ids) - 1), company_address, style=style_company_details)

    def _insert_header(self, worksheet, global_dynamic_report_id):
        font_color = global_dynamic_report_id.template_id.header_font_color or 'black'
        font_name = global_dynamic_report_id.template_id.header_font_name or 'Times New Roman'
        font_size = global_dynamic_report_id.template_id.header_font_size or '400'
        background_color = global_dynamic_report_id.template_id.header_background_color or 'white'
        if global_dynamic_report_id.template_id.is_header_italic:
            is_italic = 'on'
        else:
            is_italic = 'off'
        if global_dynamic_report_id.template_id.is_header_bold:
            is_bold = 'on'
        else:
            is_bold = 'off'
        
        style_header = xlwt.easyxf("font: color " + font_color + 
                    "; font: name " + font_name + 
                    "; font:height " + font_size + 
                    "; font: italic " + is_italic + 
                    "; font: bold " + is_bold + 
                    "; align: vert centre, horiz centre; pattern: pattern solid, pattern_fore_colour " + background_color 
                    )
        worksheet.write_merge(0, 1, 0, (len(global_dynamic_report_id.parent_object_field_ids) - 1), global_dynamic_report_id.template_id.header_title, style=style_header)

    def dynamic_print_excel_report(self):
        global_dynamic_report_id = self.env['sr.global.dynamic.excel.report'].browse(self._context.get('dynamic_report_id'))
        if global_dynamic_report_id.child_object_id:
            submodel_relation_field = global_dynamic_report_id.child_object_id.field_id.filtered(lambda l: l.relation == global_dynamic_report_id.object_id.model)
            if not submodel_relation_field:
                raise UserError('There is no any relation between parent object and child object..!')
        if not self.sheet_per_record:
            workbook = xlwt.Workbook(encoding="utf-8")
            worksheet = workbook.add_sheet(global_dynamic_report_id.template_id.excel_sheet_name)
            self._insert_header(worksheet, global_dynamic_report_id)
            if global_dynamic_report_id.template_id.is_show_company:
                self._insert_company_detail(3, 0, worksheet, global_dynamic_report_id)
                row = 14
            else:
                row = 3
            read_values = []
            if global_dynamic_report_id.groupby_parent_field_id:
                for order in self.env[self._context.get('active_model')].browse(self._context.get('active_ids')):
                    read_values.append(order.read()[0])
                sorted_value = sorted(read_values, key=lambda l: l[global_dynamic_report_id.groupby_parent_field_id.name])
                group_by = itertools.groupby(sorted_value, key=operator.itemgetter(global_dynamic_report_id.groupby_parent_field_id.name))
                groupby_values = [{global_dynamic_report_id.groupby_parent_field_id.name:k, 'values':[x for x in v]} for k, v in group_by]
                row += 1
                col = 0
                for header_field in global_dynamic_report_id.parent_object_field_ids:
                    field_header_style = xlwt.easyxf("font: bold on; font: color black; pattern: pattern solid, pattern_fore_colour gray25")
                    worksheet.write(row, col, header_field.label, style=field_header_style)
                    col += 1
                row += 2
                for value in groupby_values:
                    col = 0
                    if isinstance(value[global_dynamic_report_id.groupby_parent_field_id.name], tuple):
                        worksheet.write_merge(row, row, 0, (len(global_dynamic_report_id.parent_object_field_ids) - 1), value[global_dynamic_report_id.groupby_parent_field_id.name][1], field_header_style)
                    else:
                        worksheet.write_merge(row, row, 0, (len(global_dynamic_report_id.parent_object_field_ids) - 1), value[global_dynamic_report_id.groupby_parent_field_id.name][1], field_header_style)
                    row += 2
                    col = 0
                    for line in value.get('values'):
                        col = 0
                        for field in global_dynamic_report_id.parent_object_field_ids:
                            if isinstance(line[field.field_id.name], tuple):
                                if str(field.field_id.ttype) == 'datetime':
                                    date_value = str(line[field.field_id.name][1]).split(".")[0]
                                    user_timezone = self.env.user.tz  
                                    if  user_timezone:
                                        local_timezone = pytz.timezone(user_timezone) 
                                    else:
                                        local_timezone = 'UTC'
                                    line[field.field_id.name][1] = datetime.strftime(pytz.utc.localize(datetime.strptime(str(date_value), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local_timezone), "%d/%m/%Y %H:%M:%S")
                                
                                field_value_header_style = xlwt.easyxf("font: bold on; font: color black; pattern: pattern solid, pattern_fore_colour aqua")
                                worksheet.write(row, col, line[field.field_id.name][1], style=field_value_header_style)
                            else:
                                if str(field.field_id.ttype) == 'datetime':
                                    date_value = str(line[field.field_id.name]).split(".")[0]
                                    user_timezone = self.env.user.tz  
                                    if  user_timezone:
                                        local_timezone = pytz.timezone(user_timezone) 
                                    else:
                                        local_timezone = 'UTC'
                                    line[field.field_id.name] = datetime.strftime(pytz.utc.localize(datetime.strptime(str(date_value), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local_timezone), "%d/%m/%Y %H:%M:%S")
                                field_value_header_style = xlwt.easyxf("font: bold on; font: color black; pattern: pattern solid, pattern_fore_colour aqua")
                                worksheet.write(row, col, line[field.field_id.name], style=field_value_header_style)
                            col += 1
                        row += 2
                        col = 0
                        if global_dynamic_report_id.child_object_id:
                            child_value = self.env[global_dynamic_report_id.child_object_id.model].search([(submodel_relation_field.name, '=', line.get('id'))])
                            for child_field in global_dynamic_report_id.child_object_field_ids:
                                field_header_style = xlwt.easyxf("font: bold on; font: color black; pattern: pattern solid, pattern_fore_colour gray25")
                                worksheet.write(row, col, child_field.label, style=field_header_style)
                                col += 1
                            row += 1
                            col = 0
                            for child_line in child_value:
                                for child_field in global_dynamic_report_id.child_object_field_ids:
                                    value = getattr(child_line, child_field.field_id.name)
                                    if child_field.field_id.ttype == "many2one":
                                        value = value.name
                                    if child_field.field_id.ttype == "datetime":
                                        date_value = str(value).split(".")[0] 
                                        user_timezone = self.env.user.tz  
                                        if  user_timezone:
                                            local_timezone = pytz.timezone(user_timezone) 
                                        else:
                                            local_timezone = 'UTC'  
                                        value = datetime.strftime(pytz.utc.localize(datetime.strptime(str(date_value), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local_timezone), "%d/%m/%Y %H:%M:%S") 
                                    worksheet.write(row, col, value)
                                    col += 1
                                row += 1
                                col = 0
                            row += 1
                    row += 1
            else:
                row += 1
                col = 0
                for header_field in global_dynamic_report_id.parent_object_field_ids:
                    field_header_style = xlwt.easyxf("font: bold on; font: color black; pattern: pattern solid, pattern_fore_colour gray25")
                    worksheet.write(row, col, header_field.label, style=field_header_style)
                    col += 1
                row += 1
                col = 0
                for order in self.env[self._context.get('active_model')].browse(self._context.get('active_ids')):
                    date_value = ''
                    for header_field in global_dynamic_report_id.parent_object_field_ids:
                        value = getattr(order, header_field.field_id.name)
                        if header_field.field_id.ttype == "many2one":
                            value = value.name
                        if header_field.field_id.ttype == "datetime":
                            date_value = str(value).split(".")[0] 
                            user_timezone = self.env.user.tz  
                            if  user_timezone:
                                local_timezone = pytz.timezone(user_timezone) 
                            else:
                                local_timezone = 'UTC'  
                            value = datetime.strftime(pytz.utc.localize(datetime.strptime(str(date_value), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local_timezone), "%d/%m/%Y %H:%M:%S")
                        worksheet.write(row, col, value)
                        col += 1
                    row += 1
                    col = 0
                    if global_dynamic_report_id.child_object_id:
                        child_value = self.env[global_dynamic_report_id.child_object_id.model].search([(submodel_relation_field.name, '=', order.id)])
                        for child_field in global_dynamic_report_id.child_object_field_ids:
                            field_header_style = xlwt.easyxf("font: bold on; font: color black; pattern: pattern solid, pattern_fore_colour gray25")
                            worksheet.write(row, col, child_field.label, style=field_header_style)
                            col += 1
                        row += 1
                        col = 0
                        for child_line in child_value:
                            for child_field in global_dynamic_report_id.child_object_field_ids:
                                value = getattr(child_line, child_field.field_id.name)
                                if child_field.field_id.ttype == "many2one":
                                    value = value.name
                                if child_field.field_id.ttype == "datetime":
                                    date_value = str(value).split(".")[0] 
                                    user_timezone = self.env.user.tz  
                                    if  user_timezone:
                                        local_timezone = pytz.timezone(user_timezone) 
                                    else:
                                        local_timezone = 'UTC'  
                                    value = datetime.strftime(pytz.utc.localize(datetime.strptime(str(date_value), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local_timezone), "%d/%m/%Y %H:%M:%S") 
                                worksheet.write(row, col, value)
                                col += 1
                            row += 1
                            col = 0
                        row += 1
                total = 0
                if global_dynamic_report_id.template_id.is_print_total and not global_dynamic_report_id.child_object_id:
                    col = 0
                    row += 1
                    font_color = global_dynamic_report_id.template_id.total_Font_color or 'white'
                    background_color = global_dynamic_report_id.template_id.total_background_color or 'black'
                    total_style = xlwt.easyxf('font: bold on,color ' + font_color + ';'
                            'pattern: pattern solid, pattern_fore_colour ' + background_color)
                    for field in global_dynamic_report_id.parent_object_field_ids:
                        if field.field_id.ttype == 'monetary' or field.field_id.ttype == 'integer' or field.field_id.ttype == 'Float':
                            for order in self.env[self._context.get('active_model')].browse(self._context.get('active_ids')):
                                total += getattr(order, field.field_id.name)
                            worksheet.write(row, col, total, total_style)
                        col += 1
        else:
            read_values = []
            workbook = xlwt.Workbook(encoding="utf-8")
            for order in self.env[self._context.get('active_model')].browse(self._context.get('active_ids')):
                worksheet = workbook.add_sheet(order.name)
                self._insert_header(worksheet, global_dynamic_report_id)
                if global_dynamic_report_id.template_id.is_show_company:
                    self._insert_company_detail(3, 0, worksheet, global_dynamic_report_id)
                    row = 14
                else:
                    row = 3
                col = 0
                for header_field in global_dynamic_report_id.parent_object_field_ids:
                    field_header_style = xlwt.easyxf("font: bold on; font: color black; pattern: pattern solid, pattern_fore_colour gray25")
                    worksheet.write(row, col, header_field.label, style=field_header_style)
                    col += 1
                row += 1
                col = 0
                for header_field in global_dynamic_report_id.parent_object_field_ids:
                    value = getattr(order, header_field.field_id.name)
                    if header_field.field_id.ttype == "many2one":
                        value = value.name
                    if header_field.field_id.ttype == "datetime":
                        date_value = str(value).split(".")[0] 
                        user_timezone = self.env.user.tz  
                        if  user_timezone:
                            local_timezone = pytz.timezone(user_timezone) 
                        else:
                            local_timezone = 'UTC'  
                        value = datetime.strftime(pytz.utc.localize(datetime.strptime(str(date_value), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local_timezone), "%d/%m/%Y %H:%M:%S")
                    worksheet.write(row, col, value)
                    col += 1
                row += 1
                col = 0
                if global_dynamic_report_id.child_object_id:
                    child_value = self.env[global_dynamic_report_id.child_object_id.model].search([(submodel_relation_field.name, '=', order.id)])
                    for child_field in global_dynamic_report_id.child_object_field_ids:
                        field_header_style = xlwt.easyxf("font: bold on; font: color black; pattern: pattern solid, pattern_fore_colour gray25")
                        worksheet.write(row, col, child_field.label, style=field_header_style)
                        col += 1
                    row += 1
                    col = 0
                    for child_line in child_value:
                        for child_field in global_dynamic_report_id.child_object_field_ids:
                            value = getattr(child_line, child_field.field_id.name)
                            if child_field.field_id.ttype == "many2one":
                                value = value.name
                            if child_field.field_id.ttype == "datetime":
                                date_value = str(value).split(".")[0] 
                                user_timezone = self.env.user.tz  
                                if  user_timezone:
                                    local_timezone = pytz.timezone(user_timezone) 
                                else:
                                    local_timezone = 'UTC'  
                                value = datetime.strftime(pytz.utc.localize(datetime.strptime(str(date_value), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local_timezone), "%d/%m/%Y %H:%M:%S") 
                            worksheet.write(row, col, value)
                            col += 1
                        row += 1
                        col = 0
                    row += 1

        file_data = io.BytesIO()
        workbook.save(file_data)
        self.write({
            'state': 'get',
            'data': base64.b64encode(file_data.getvalue()),
            'name': "Global Dynamic Excel Report.xlsx"
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Global Dynamic Excel Report',
            'res_model': 'sr.global.excel.report.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'new'
        }
