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
import csv
import sys
import xlrd
import base64
import tempfile
import binascii
from odoo import models, fields, _
from odoo.exceptions import UserError, ValidationError


class Import_Product(models.TransientModel):
    _name = 'import.product.supplier'
    _description = 'Import Product supplier'

    file = fields.Binary('File')
    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select', default='csv')

    def create_product_supplier(self, line):
        partner_id = self.env['res.partner'].search([('name', '=', line[1])])
        if not partner_id:
            raise UserError(_('%s Vendor is not exist' % line[1]))
        if len(partner_id.ids) >= 2:
            raise UserError(_('Found Multiple Vendor - %s' % line[1]))
        brand_id = self.env['product.brand'].search([('name', '=', line[2])])
        if not brand_id:
            raise UserError(_('%s Brand is not exist' % line[2]))
        if len(brand_id.ids) >= 2:
            raise UserError(_('Found Multiple Brand - %s' % line[2]))
        code = line[3]
        if '.' in line[3]:
            code = line[3].split('.')[0]
        product_id = self.env['product.product'].search([('default_code', '=', code)])
        if not product_id:
            raise UserError(_('%s Amicco SKU Code is not exist' % code))
        if len(product_id.ids) >= 2:
            raise UserError(_('Found Multiple Amicco SKU Code - %s' % code))
        self.env['product.supplierinfo'].create({
            'priority': int(float(line[0])) if line[0] else 0,
            'partner_id': partner_id.id or False,
            'brand_id': brand_id.id or False,
            'product_id': product_id.id or False,
            'ap': int(float(line[4])) if line[4] else 0,
            'gp': int(float(line[5])) if line[5] else 0
        })
        return

    def import_product_supplier(self):
        try:
            if self.import_option == 'xls':
                try:
                    fp = tempfile.NamedTemporaryFile(suffix=".xls")
                    fp.write(binascii.a2b_base64(self.file))
                    fp.seek(0)
                    workbook = xlrd.open_workbook(fp.name)
                    sheet = workbook.sheet_by_index(0)
                    for row_no in range(sheet.nrows):
                        val = {}
                        if row_no <= 0:
                            fields = list(map(lambda row:row.value.encode('utf-8'), sheet.row(row_no)))
                        else:
                            line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                            self.create_product_supplier(line)
                except Exception as e:
                    raise UserError(_(e))
            else:
                try:
                    csv_data = base64.b64decode(self.file)
                    data_file = io.StringIO(csv_data.decode("utf-8"))
                    data_file.seek(0)
                    file_reader = []
                    csv_reader = csv.reader(data_file, delimiter=',')
                    file_reader.extend(csv_reader)
                except:
                    raise UserError(_("Invalid file!"))
    
                for i in range(len(file_reader)):
                    line = list(map(str, file_reader[i]))
                    if line:
                        if i == 0:
                            continue
                        else:
                            self.create_product_supplier(line)
        except Exception as e:
            raise UserError(_(e))
