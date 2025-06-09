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
import openpyxl
import base64
import tempfile
import binascii
from odoo.exceptions import UserError
from odoo import models, fields, api, _


class ImportInventoryAdjustment(models.TransientModel):
    _name = 'import.inventory.adjustment'
    _description = 'Import Inventory Adjustment'

    import_file = fields.Binary('File')
    import_file_by = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select File', default='csv')
    import_product_option = fields.Selection([('name', 'Name'), ('code', 'Code'), ('barcode', 'Barcode')],
                                             string='Import Product By', default='name')
    location_id = fields.Many2one('stock.location', string='Select Inventory Location', required=True,
                                  domain="[('usage', 'in', ['internal', 'transit'])]")
    inventory_name = fields.Char(string='Inventory Adjustment Name', required=False)

    def import_inventory_adjustment(self):
        try:
            if self.import_file_by == 'xls':
                fp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
                fp.write(binascii.a2b_base64(self.import_file))
                fp.seek(0)
                workbook = openpyxl.load_workbook(fp.name, data_only=True)
                sheet = workbook.active
                for row_no, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                    if row_no == 1:
                        continue
                    product_val = row[0]
                    qty = row[1]
                    if product_val:
                        p_id = self._find_product(product_val)
                        inventory = self.env['stock.quant'].create({
                            'product_id': p_id.id,
                            'inventory_quantity': qty,
                            'location_id': self.location_id.id,
                        })
                        inventory.action_apply_inventory()
                    else:
                        raise UserError(_('Product name is required.'))
            else:
                keys = ['product_name', 'qty']
                try:
                    csv_data = base64.b64decode(self.import_file)
                    data_file = io.StringIO(csv_data.decode("utf-8"))
                    data_file.seek(0)
                    file_reader = []
                    csv_reader = csv.reader(data_file, delimiter=',')
                    file_reader.extend(csv_reader)
                except Exception as e:
                    raise UserError(_("Invalid file! Error: %s" % str(e)))

                for i, field in enumerate(file_reader):
                    values = dict(zip(keys, field))
                    if values:
                        if i == 0:
                            continue
                        if values.get('product_name'):
                            p_id = self._find_product(values.get('product_name'))
                            inventory = self.env['stock.quant'].create({
                                'product_id': p_id.id,
                                'inventory_quantity': values.get('qty'),
                                'location_id': self.location_id.id,
                            })
                            inventory.action_apply_inventory()
                        else:
                            raise UserError(_('Product name is required.'))
        except Exception as e:
            raise UserError(_("Error: %s" % str(e)))

    def _find_product(self, product):
        domain = []
        if self.import_product_option == 'name':
            domain = [('name', '=', product)]
        elif self.import_product_option == 'code':
            domain = [('default_code', '=', product)]
        else:
            domain = [('barcode', '=', product)]

        product_id = self.env['product.product'].search(domain, limit=1)
        if not product_id:
            raise UserError(_('Product "%s" not found in the system.' % product))
        return product_id
