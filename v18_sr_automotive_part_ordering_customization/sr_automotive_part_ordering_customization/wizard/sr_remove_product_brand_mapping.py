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


class removeProductBrandMapping(models.TransientModel):
    _name = 'remove.product.brand.mapping'
    _description = 'Remove Product Brand Mapping'

    file = fields.Binary('File')
    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select', default='csv')

    def remove_product_brand_mapping(self, line):
        try:
            model_data = self.env.ref(line[0])
        except:
            return
        if model_data:
            model_data.unlink()
        return

    def import_remove_product_brand_mapping(self):
        if self.import_option == 'xls':
            try:
                fp = tempfile.NamedTemporaryFile(suffix=".xls")
                fp.write(binascii.a2b_base64(self.file))
                fp.seek(0)
                workbook = xlrd.open_workbook(fp.name)
                sheet = workbook.sheet_by_index(0)
            except:
                raise ValidationError(_("Invalid file!"))

            for row_no in range(sheet.nrows):
                val = {}
                if row_no <= 0:
                    fields = list(map(lambda row: row.value.encode('utf-8'), sheet.row(row_no)))
                else:
                    line = list(
                        map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value),
                            sheet.row(row_no)))
                    self.remove_product_brand_mapping(line)
        else:
            try:
                csv_data = base64.b64decode(self.file)
                data_file = io.StringIO(csv_data.decode("utf-8"))
                data_file.seek(0)
                file_reader = []
                csv_reader = csv.reader(data_file, delimiter=',')
                file_reader.extend(csv_reader)
            except:
                raise ValidationError(_("Invalid file!"))

            for i in range(len(file_reader)):
                line = list(map(str, file_reader[i]))
                if line:
                    if i == 0:
                        continue
                    else:
                        self.remove_product_brand_mapping(line)
