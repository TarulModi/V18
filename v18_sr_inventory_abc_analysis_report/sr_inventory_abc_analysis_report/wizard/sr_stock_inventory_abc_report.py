# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, models, api, _
import base64
from odoo.exceptions import ValidationError

try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')
try:
    import io
except ImportError:
    _logger.debug('Cannot `import io`.')
    

class srABCExcelReport(models.TransientModel):
    _name = "sr.abc.excel.report"
    _description = "ABC Excel Report"

    excel_file = fields.Binary('Excel Report')
    file_name = fields.Char('Excel File', size=64)

#Stock Invenotry ABC Report Class
class srStockInventoryABCReport(models.TransientModel):
    _name = "stock.inventory.abc.report"
    _description = "Stock Inventory ABC Report"

    from_date = fields.Date("From Date")
    to_date = fields.Date("To Date")
    abc_base_on = fields.Selection(
        [("products", "Products"), ("product_categ", "Product Categories")],
        default="products",
    )
    classification_by = fields.Selection(
        [("sold_unit", "Sold Units"), ("consumption_value", "Consumption Value")],
        default="sold_unit",
    )
    
    @api.onchange("from_date")
    def _from_date_onchange(self):
        if self.to_date and self.from_date > self.to_date:
            raise ValidationError(_("Please select the correct start date."))
    
    @api.onchange("to_date")
    def _to_date_onchange(self):
        if self.from_date and self.from_date > self.to_date:
            raise ValidationError(_("Please select the correct end date."))

    #Print PDF Report Function
    def print_report_pdf(self):
        data = {}
        return self.env.ref(
            "sr_inventory_abc_analysis_report.sr_inventory_abc_analysis_report_template"
        ).report_action(None, data=data)

    #Print Excel Report Function
    def print_report_excel(self):
        datas = self.env["report.sr_inventory_abc_analysis_report.abc_template"]._get_report_values(docids=self.ids)["items_data"]
        filename = "ABC Report.xls"
        workbook = xlwt.Workbook("stock_inventory_abc_report.xlsx")
        worksheet = workbook.add_sheet("Stock Inventory ABC Analysis Report")
        
        HEADER = xlwt.easyxf(
            'font: bold 1, height 200;'
            'align: vertical center, horizontal center, wrap on;'
            'borders: top double, bottom double, left double, right double;'
            )
        
        TABLE_HEADER = xlwt.easyxf(
            'font: bold 1;'
            'align: vertical center, horizontal center, wrap on;'
            )
            
        REPORT_DETAILS = xlwt.easyxf(
            'align: vertical center, horizontal center, wrap on;'
            )
        
        abc_base_on = dict(self._fields['abc_base_on'].selection).get(self.abc_base_on)
        classification_by = dict(self._fields['classification_by'].selection).get(self.classification_by)
        
        if self.classification_by == "sold_unit":
            worksheet.write_merge(0, 2, 0, 7, "Stock Inventory ABC Analysis Report", HEADER)
            worksheet.write_merge(4, 4, 0, 1, "Based On", TABLE_HEADER)
            worksheet.write_merge(4, 4, 2, 3, "Classification By", TABLE_HEADER)
            worksheet.write_merge(4, 4, 4, 5, "From Date", TABLE_HEADER)
            worksheet.write_merge(4, 4, 6, 7, "To Date", TABLE_HEADER)
        
            worksheet.write_merge(5, 5, 0, 1, abc_base_on, REPORT_DETAILS)
            worksheet.write_merge(5, 5, 2, 3, classification_by, REPORT_DETAILS)
            worksheet.write_merge(5, 5, 4, 5, str(self.from_date), REPORT_DETAILS)
            worksheet.write_merge(5, 5, 6, 7, str(self.to_date), REPORT_DETAILS)
        
        row = 8
        total_sold_units = 0
        total_consumption_value = 0

        if self.abc_base_on == "products":
            if self.classification_by == "sold_unit":
                #Report table header details
                worksheet.write_merge(7, 7, 0, 1, "Products", TABLE_HEADER)
                worksheet.write_merge(7, 7, 2, 3, "Sold Units", TABLE_HEADER)
                worksheet.write_merge(7, 7, 4, 5, "% Sold Units", TABLE_HEADER)
                worksheet.write_merge(7, 7, 6, 7, "Classification", TABLE_HEADER)

                if datas:
                    for item in datas:
                        per_of_sold_unit = "{:.2f}".format(item.get("per_of_sold_unit"))
                        worksheet.write_merge(row, row, 0, 1, item.get("product"), REPORT_DETAILS)
                        worksheet.write_merge(row, row, 2, 3, item.get("product_qty"), REPORT_DETAILS)
                        worksheet.write_merge(row, row, 4, 5, per_of_sold_unit, REPORT_DETAILS)
                        worksheet.write_merge(row, row, 6, 7, item.get("classification"), REPORT_DETAILS)
                        row += 1
                        total_sold_units += item.get("product_qty")
                    if total_sold_units:
                        row += 1
                        worksheet.write_merge(row, row, 0, 1, "Total Sold Units", TABLE_HEADER)
                        worksheet.write_merge(row, row, 2, 3, total_sold_units, TABLE_HEADER)
            else:
                #Report header details
                worksheet.write_merge(0, 2, 0, 11, "Stock Inventory ABC Analysis Report", HEADER)
                worksheet.write_merge(4, 4, 0, 2, "Based On", TABLE_HEADER)
                worksheet.write_merge(4, 4, 3, 5, "Classification By", TABLE_HEADER)
                worksheet.write_merge(4, 4, 6, 8, "From Date", TABLE_HEADER)
                worksheet.write_merge(4, 4, 9, 11, "To Date", TABLE_HEADER)
        
                worksheet.write_merge(5, 5, 0, 2, abc_base_on, REPORT_DETAILS)
                worksheet.write_merge(5, 5, 3, 5, classification_by, REPORT_DETAILS)
                worksheet.write_merge(5, 5, 6, 8, str(self.from_date), REPORT_DETAILS)
                worksheet.write_merge(5, 5, 9, 11, str(self.to_date), REPORT_DETAILS)
            
                #Report table header details
                worksheet.write_merge(7, 7, 0, 1, "Products", TABLE_HEADER)
                worksheet.write_merge(7, 7, 2, 3, "Sold Units", TABLE_HEADER)
                worksheet.write_merge(7, 7, 4, 5, "Cost Per Unit", TABLE_HEADER)
                worksheet.write_merge(7, 7, 6, 7, "Consumption Value", TABLE_HEADER)
                worksheet.write_merge(7, 7, 8, 9, "% Consumption Value", TABLE_HEADER)
                worksheet.write_merge(7, 7, 10, 11, "Classification", TABLE_HEADER)

                if datas:
                    for item in datas:
                        per_of_consumption_value = "{:.2f}".format(item.get("per_of_consumption_value"))
                        worksheet.write_merge(row, row, 0, 1, item.get("product"), REPORT_DETAILS)
                        worksheet.write_merge(row, row, 2, 3, item.get("product_qty"), REPORT_DETAILS)
                        worksheet.write_merge(row, row, 4, 5, item.get("product_cost"), REPORT_DETAILS)
                        worksheet.write_merge(row, row, 6, 7, item.get("consumption_value"), REPORT_DETAILS)
                        worksheet.write_merge(row, row, 8, 9, per_of_consumption_value, REPORT_DETAILS)
                        worksheet.write_merge(row, row, 10, 11, item.get("classification"), REPORT_DETAILS)
                        row += 1
                        total_consumption_value += item.get("consumption_value")
                    if total_consumption_value:
                        row += 1
                        worksheet.write_merge(row, row, 0, 1, "Total Consumption Value", TABLE_HEADER)
                        worksheet.write_merge(row, row, 6, 7, total_consumption_value, TABLE_HEADER)
        else:
            if self.classification_by == "sold_unit":
                worksheet.write_merge(7, 7, 0, 1, "Product Categories", TABLE_HEADER)
                worksheet.write_merge(7, 7, 2, 3, "Sold Units", TABLE_HEADER)
                worksheet.write_merge(7, 7, 4, 5, "% Sold Units", TABLE_HEADER)
                worksheet.write_merge(7, 7, 6, 7, "Classification", TABLE_HEADER)
                
                if datas:
                    for item in datas:
                        per_of_sold_unit = "{:.2f}".format(item.get("per_of_sold_unit"))
                        worksheet.write_merge(row, row, 0, 1, item.get("category_name"), REPORT_DETAILS)
                        worksheet.write_merge(row, row, 2, 3, item.get("category_sold_units"), REPORT_DETAILS)
                        worksheet.write_merge(row, row, 4, 5, per_of_sold_unit, REPORT_DETAILS)
                        worksheet.write_merge(row, row, 6, 7, item.get("classification"), REPORT_DETAILS)
                        row += 1
                        total_sold_units += item.get("category_sold_units")
                    if total_sold_units:
                        row += 1
                        worksheet.write_merge(row, row, 0, 1, "Total Sold Units", TABLE_HEADER)
                        worksheet.write_merge(row, row, 2, 3, total_sold_units, TABLE_HEADER)
            else:
                #Report header details
                worksheet.write_merge(0, 2, 0, 9, "Stock Inventory ABC Analysis Report", HEADER)
                worksheet.write_merge(4, 4, 0, 2, "Based On", TABLE_HEADER)
                worksheet.write_merge(4, 4, 3, 5, "Classification By", TABLE_HEADER)
                worksheet.write_merge(4, 4, 6, 7, "From Date", TABLE_HEADER)
                worksheet.write_merge(4, 4, 8, 9, "To Date", TABLE_HEADER)
        
                worksheet.write_merge(5, 5, 0, 2, abc_base_on, REPORT_DETAILS)
                worksheet.write_merge(5, 5, 3, 5, classification_by, REPORT_DETAILS)
                worksheet.write_merge(5, 5, 6, 7, str(self.from_date), REPORT_DETAILS)
                worksheet.write_merge(5, 5, 8, 9, str(self.to_date), REPORT_DETAILS)
                
                #Report table header details
                worksheet.write_merge(7, 7, 0, 1, "Product Categories", TABLE_HEADER)
                worksheet.write_merge(7, 7, 2, 3, "Sold Units", TABLE_HEADER)
                worksheet.write_merge(7, 7, 4, 5, "Consumption Value", TABLE_HEADER)
                worksheet.write_merge(7, 7, 6, 7, "% Consumption Value", TABLE_HEADER)
                worksheet.write_merge(7, 7, 8, 9, "Classification", TABLE_HEADER)

                if datas:
                    for item in datas:
                        per_of_consumption_value = "{:.2f}".format(item.get("per_of_consumption_value"))
                        worksheet.write_merge(row, row, 0, 1, item.get("category_name"), REPORT_DETAILS)
                        worksheet.write_merge(row, row, 2, 3, item.get("category_sold_units"), REPORT_DETAILS)
                        worksheet.write_merge(row, row, 4, 5, item.get("category_consumption_value"), REPORT_DETAILS)
                        worksheet.write_merge(row, row, 6, 7, per_of_consumption_value, REPORT_DETAILS)
                        worksheet.write_merge(row, row, 8, 9, item.get("classification"), REPORT_DETAILS)
                        row += 1
                        total_consumption_value += item.get("category_consumption_value")
                    if total_consumption_value:
                        row += 1
                        worksheet.write_merge(row, row, 0, 1, "Total Consumption Value", TABLE_HEADER)
                        worksheet.write_merge(row, row, 4, 5, total_consumption_value, TABLE_HEADER)
        
        fp = io.BytesIO()
        workbook.save(fp)
        export_id = self.env['sr.abc.excel.report'].create(
            {'excel_file': base64.b64encode(fp.getvalue()), 'file_name': filename})
        res = {
            'name' : 'Inventory ABC Excel Report',
            'view_mode': 'form',
            'res_id': export_id.id,
            'res_model': 'sr.abc.excel.report',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new'
        }
        return res
