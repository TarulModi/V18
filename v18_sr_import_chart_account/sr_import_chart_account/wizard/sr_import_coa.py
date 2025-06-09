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
import openpyxl
from odoo.exceptions import UserError
from odoo import models, fields, api, _


class ImportCOA(models.TransientModel):
    _name = 'import.coa'
    _description = 'Import Charts of Accounts'

    file = fields.Binary('File')
    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select File', default='xls')

    def find_currency(self, currency):
        if not currency:
            return False
        currency_id = self.env['res.currency'].search([('name', '=', currency)])
        if currency_id:
            return currency_id.id
        else:
            raise UserError(_('%s currency does not exist in system' % currency))

    def find_company(self, company):
        company_ids = self.env['res.company'].search([('name', 'in', company.split(','))])
        if company_ids:
            return [(6, 0, company_ids.ids)]
        else:
            raise UserError(_('%s Company/Companies do not exist in the system.' % company))


    def find_tags(self, tags_ids):
        tag_ids = []
        if tags_ids:
            tags = tags_ids.split(',')
            for name in tags:
                tag = self.env['account.account.tag'].search([('name', '=', name)])
                if not tag:
                    raise Warning(_('"%s" tag not in your system') % name)
                tag_ids.append(tag[0].id)
        return [(6, 0, tag_ids)]
    
    def find_taxes(self, taxes_ids):
        tax_ids = []
        if taxes_ids:
            taxes = taxes_ids.split(',')
            for name in taxes:
                tax = self.env['account.tax'].search([('name', '=', name)])
                if not tax:
                    raise Warning(_('"%s" Tax not in your system') % name)
                tax_ids.append(tax[0].id)
        return [(6, 0, tax_ids)]

    def find_user_type(self, type_id):
        # user_type_id = self.env['account.account.type'].search([('name', '=', type_id)])
        model = self.env['account.account']
        for key, display_name in model.fields_get('account_type')['account_type']['selection']:
            if display_name == type_id:
                return key
        user_type_id = self.env['account.account'].search([('account_type', '=', type_id)])
        if user_type_id:
            return user_type_id.id
        else:
            raise UserError(_('%s User Type does not exist in system' % type_id))

    def create_coa(self, line):
        try:
            code = int(float(line[0]))
        except ValueError:
            raise UserError(_("Invalid code value: %s. The code must be numeric." % line[0]))
        
        self.env['account.account'].create({
            'code': code,
            'name': line[1],
            'account_type': self.find_user_type(line[2]),
            'tax_ids': self.find_taxes(line[3]),
            'tag_ids': self.find_tags(line[4]),
            'company_ids': self.find_company(line[5]),
            'currency_id': self.find_currency(line[6]),
            'reconcile': True if line[7] == '1' else False,
            'deprecated': True if line[8] == '1' else False,
        })
        
    def import_coa(self):
        try:
            if self.import_option == 'xls':
                fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
                fp.write(binascii.a2b_base64(self.file))
                fp.seek(0)
                workbook = openpyxl.load_workbook(fp.name, data_only=True)
                sheet = workbook.active
                for row_no, row in enumerate(sheet.iter_rows(values_only=True)):
                    if row_no == 0:
                        continue
                    else:
                        line = [str(cell).strip() if cell is not None else '' for cell in row]
                        self.create_coa(line)
            else:
                csv_data = base64.b64decode(self.file)
                data_file = io.StringIO(csv_data.decode("utf-8"))
                csv_reader = csv.reader(data_file, delimiter=',')
                for i, line in enumerate(csv_reader):
                    if i == 0:
                        continue
                    self.create_coa(line)
        except Exception as e:
            raise UserError(_("Import Error: %s") % str(e))
    
