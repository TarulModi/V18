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
import base64
import logging
import openpyxl
from datetime import datetime
from odoo.exceptions import UserError
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class srImportJournalEntry(models.TransientModel):
    _name = 'import.journal.entry'
    _description = 'Import Journal Entry'

    file = fields.Binary('File')
    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select', default='csv')
    status = fields.Selection([('draft', 'Draft'), ('post', 'Post')], string='Status', default='draft')

    def _find_partner(self, customer):
        if not customer:
            return False
        partner_id = self.env['res.partner'].search([('name', '=', customer)], limit=1)
        if partner_id:
            return partner_id.id
        else:
            raise UserError(_('%s customer does not exist in system' % customer))

    def _find_journal(self, journal):
        if not journal:
            return False
        journal_id = self.env['account.journal'].search([('name', '=', journal)], limit=1)
        if journal_id:
            return journal_id.id
        else:
            raise UserError(_('%s journal does not exist in system' % journal))

    def _find_account(self, account):
        if not account:
            return False
        account_id = self.env['account.account'].search([('code', '=', account)], limit=1)
        if account_id:
            return account_id.id
        else:
            raise UserError(_('%s account does not exist in system' % account))

    def _find_currency(self, currency):
        if not currency:
            return False
        currency_id = self.env['res.currency'].search([('name', '=', currency)], limit=1)
        if currency_id:
            return currency_id.id
        else:
            raise UserError(_('%s account does not exist in system' % currency))

    @api.model
    def _import_csv(self, file_data):
        data = base64.b64decode(file_data)
        io_file = io.StringIO(data.decode('utf-8'))
        reader = csv.DictReader(io_file)
        return list(reader)

    @api.model
    def _import_xlsx(self, file_data):
        data = base64.b64decode(file_data)
        file_obj = io.BytesIO(data)
        wb = openpyxl.load_workbook(file_obj, data_only=True)
        sheet = wb.active
        rows = list(sheet.iter_rows(min_row=2, values_only=True))
        headers = ['name', 'Reference', 'Partner', 'Date', 'Journal', 'Account', 'Label', 'Debit', 'Credit',
                   'Amount Currency', 'Currency']

        def parse_date(date_value):
            if isinstance(date_value, str):
                try:
                    return datetime.strptime(date_value, '%d/%m/%Y')
                except ValueError:
                    return None
            elif isinstance(date_value, (float, int)):
                return openpyxl.utils.datetime.from_excel(date_value)
            else:
                return None

        parsed_rows = []
        for row in rows:
            row_dict = dict(zip(headers, row))
            row_dict['Date'] = parse_date(row_dict['Date'])
            parsed_rows.append(row_dict)
        return parsed_rows

    def _process_data(self, records):
        grouped_data = {}

        for record in records:
            num = record.get('name') or record.get('Number')
            date = record['Date']

            if isinstance(date, str):
                try:
                    date = datetime.strptime(date, '%d/%m/%Y')
                except ValueError:
                    _logger.error(f"Invalid date format for {record['Partner']}: {date}")
                    date = None
            elif isinstance(date, datetime):
                pass
            else:
                date = None

            if num not in grouped_data:
                grouped_data[num] = {
                    'name': num,
                    'entries': [],
                    'partner': record['Partner'],
                    'date': date,
                    'journal': record['Journal'],
                    'reference': record['Reference'],
                }

            grouped_data[num]['entries'].append({
                'account': record['Account'],
                'label': record['Label'],
                'debit': float(record['Debit']) if record['Debit'] else 0,
                'credit': float(record['Credit']) if record['Credit'] else 0,
                'amount_currency': record['Amount Currency'],
                'currency': record['Currency']
            })
        return grouped_data

    def _create_journal_entries(self, grouped_data):
        for num, group in grouped_data.items():
            journal_entry_vals = {
                'name' : num,
                'partner_id': self._find_partner(group['partner']),
                'date': group['date'].strftime('%Y-%m-%d') if group['date'] else fields.Date.today(),
                'journal_id': self._find_journal(group['journal']),
                'ref': group['reference'],
                'line_ids': [],
            }

            for entry in group['entries']:
                journal_entry_vals['line_ids'].append((0, 0, {
                    'account_id': self._find_account(entry['account']),
                    'name': entry['label'],
                    'debit': entry['debit'],
                    'credit': entry['credit'],
                    'currency_id': self._find_currency(entry['currency']),
                }))
            move_id = self.env['account.move'].create(journal_entry_vals)
            if move_id and self.status == 'post':
                move_id.action_post()

    def import_journal_entry(self):
        if not self.file:
            raise UserError(_('Please upload a file to import.'))

        file_data = self.file
        if self.import_option == 'csv':
            records = self._import_csv(file_data)
        else:
            records = self._import_xlsx(file_data)

        grouped_data = self._process_data(records)
        self._create_journal_entries(grouped_data)
        return {'type': 'ir.actions.act_window_close'}
