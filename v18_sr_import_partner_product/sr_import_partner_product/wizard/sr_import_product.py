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
import os
import csv
import sys
import xlrd
import base64
import openpyxl
import tempfile
import binascii
from odoo import models, fields, _
from odoo.exceptions import UserError, ValidationError


class Import_Product(models.TransientModel):
    _name = 'import.product'
    _description = 'Import Product'

    file = fields.Binary('File')
    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select', default='csv')
    create_update_option = fields.Selection([('create', 'Create Product'), ('update', 'Update Product')], string='Option', default='create')

    def create_product(self, line):
        is_storable = False
        if line[1] == 'Consumable':
            type_value = 'consu'
        elif line[1] == 'Service':
            type_value = 'service'
        else:
            type_value = 'consu'
            is_storable = True
        categ_id = self.env['product.category'].search([('name', '=', line[4])])
        if not categ_id:
            raise UserError(_('%s category is not exist' % line[4]))
            
        uom_id = self.env['uom.uom'].search([('name', '=', line[7])])
        if not uom_id:
            raise UserError(_('%s UOM is not exist' % line[7]))
        purchase_uom_id = self.env['uom.uom'].search([('name', '=', line[8])])
        if not purchase_uom_id:
            raise UserError(_('%s Purchase UOM is not exist' % line[8]))
        if self.create_update_option == 'create':
            product_ids = False
            product_id = False
            barcode = line[3].split('.')[0] if line[3] else ''
            if barcode:
                product_ids = self.env['product.product'].search([('barcode', '=', barcode)], limit="1")
            if line[2]:
                product_id = self.env['product.product'].search([('default_code', '=', line[2])], limit="1")
            if product_ids and product_ids.barcode or product_id and product_id.default_code:
                if product_id:
                    raise UserError(_('%s-product internal reference is already exist' % line[2]))
                else:
                    raise UserError(_('%s-product barcode is already exist' % barcode))
            else:
                self.env['product.product'].create({
                    'name':line[0],
                    'type':type_value,
                    'default_code':line[2],
                    'barcode':line[3].split('.')[0] if line[3] else '',
                    'categ_id':categ_id.id,
                    'lst_price':line[5],
                    'standard_price':line[6],
                    'uom_id':uom_id.id,
                    'uom_po_id':purchase_uom_id.id,
                    'is_storable': is_storable,
                    })
        else:
            product = self.env['product.product'].search([('name', '=', line[0])])
            if product:
                product.update({
                'type':type_value,
                'default_code':line[2],
                'barcode':line[3].split('.')[0] if line[3] else '',
                'categ_id':categ_id.id,
                'lst_price':line[5],
                'standard_price':line[6],
                'uom_id':uom_id.id,
                'uom_po_id':purchase_uom_id.id,
                'is_storable': is_storable,
                })
            else:
                raise UserError(_('%s product is not exist' % line[0]))

    def import_product(self):
        try:
            if self.import_option == 'xls':
                try:
                    fp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
                    fp.write(binascii.a2b_base64(self.file))
                    fp.close()
                    workbook = openpyxl.load_workbook(fp.name, data_only=True)
                    sheet = workbook.active
                    for row_no, row in enumerate(sheet.iter_rows(values_only=True)):
                        if row_no == 0:
                            fields = list(row)
                        else:
                            line = [str(cell) if cell is not None else '' for cell in row]
                            self.create_product(line)
                    os.unlink(fp.name)
                except Exception as e:
                    raise UserError(_("Error during Excel import: %s" % str(e)))
            else:
                try:
                    csv_data = base64.b64decode(self.file)
                    data_file = io.StringIO(csv_data.decode("utf-8"))
                    csv_reader = csv.reader(data_file, delimiter=',')
                    for i, row in enumerate(csv_reader):
                        if i == 0:
                            continue
                        self.create_product(row)
                except Exception as e:
                    raise UserError(_("Error during CSV import: %s" % str(e)))
        except Exception as e:
            raise UserError(_("Unexpected Error: %s" % str(e)))
