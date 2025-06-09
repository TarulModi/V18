# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

import base64
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class srStockInventoryTurnoverReport(models.TransientModel):
    _name = 'stock.inventory.turnover.report'
    _description = "Inventory Turnover Analyse Report"

    start_date = fields.Date()
    end_date = fields.Date()
    product_ids = fields.Many2many('product.product')
    categ_ids = fields.Many2many('product.category')
    warehouse_ids = fields.Many2many('stock.warehouse')
    company_ids = fields.Many2many('res.company')

    @api.onchange("start_date")
    def _start_date_onchange(self):
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError(_("Please select the correct start date."))

    @api.onchange("end_date")
    def _end_date_onchange(self):
        if self.start_date and self.start_date > self.end_date:
            raise ValidationError(_("Please select the correct end date."))

    def report_generate_pdf(self):
        data = {}
        return self.env.ref(
            'sr_inventory_turnover_analysis_report.sr_stock_inventory_turnover_report_template').report_action(None,
                                                                                                               data=data)

    def report_generate_excel(self):
        datas = self.env['report.sr_inventory_turnover_analysis_report.turnover']._get_report_values(docids=self.ids)[
            'print_data']
        workbook = xlsxwriter.Workbook('stock_inventory_turnover.xlsx')
        worksheet = workbook.add_worksheet()
        header_merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        worksheet.merge_range('A1:G1', 'Inventory Turnove Analysis Report', header_merge_format)
        date_format = workbook.add_format({'num_format': 'dd/mm/yy'})
        worksheet.write(1, 0, 'Start Date')
        worksheet.write(1, 1, self.start_date, date_format)

        worksheet.write(1, 3, 'End Date')
        worksheet.write(1, 4, self.end_date, date_format)

        row = 4
        worksheet.write(3, 0, 'Product')
        worksheet.write(3, 1, 'Opening Stock')
        worksheet.write(3, 2, 'Closing Stock')
        worksheet.write(3, 3, 'Average Inventory')
        worksheet.write(3, 4, 'Sales')
        worksheet.write(3, 5, 'Purchase')
        worksheet.write(3, 6, 'Inventory ratio')
        floating_point_format = workbook.add_format({'num_format': '#,##0.00', 'align': 'center',
                                                     'valign': 'vcenter', })
        for item in datas:
            worksheet.write(row, 0, item.get('name'))
            worksheet.write(row, 1, item.get('opening_stock'), floating_point_format)
            worksheet.write(row, 2, item.get('closing_stock'), floating_point_format)
            worksheet.write(row, 3, item.get('average_inventory'), floating_point_format)
            worksheet.write(row, 4, item.get('sales'), floating_point_format)
            worksheet.write(row, 5, item.get('purchase'), floating_point_format)
            worksheet.write(row, 6, item.get('inventory_turnover_ratio'), floating_point_format)
            row += 1
        workbook.close()

        file = open('stock_inventory_turnover.xlsx', 'rb').read()

        attachment = self.env['ir.attachment'].create({
            'name': 'stock_inventory_turnover.xlsx',
            'datas': base64.encodebytes(file),
            'res_id': self.id,
            'res_model': 'stock.inventory.turnover.report',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/export/%s' % attachment.id,
            'target': 'new',
        }
