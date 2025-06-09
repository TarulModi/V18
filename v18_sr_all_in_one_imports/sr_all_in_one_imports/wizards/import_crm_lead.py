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
import xlrd
import base64
from odoo.exceptions import UserError
from odoo import models, fields, api, _


class SrImportCRMLead(models.TransientModel):
    _name = "sr.import.crm.lead"
    _description = "Import CRM Lead"

    select_file = fields.Binary('File')
    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select', default='csv')

    def _find_partner(self, customer):
        if not customer:
            return False
        partner_id = self.env['res.partner'].search([('name', '=', customer)], limit=1)
        if partner_id:
            return partner_id.id
        else:
            raise UserError(_('%s customer does not exist in system' % customer))

    def _find_state(self, state):
        if not state:
            return False
        state_id = self.env['res.country.state'].search([('name', '=', state)], limit=1)
        if state_id:
            return state_id.id
        else:
            raise UserError(_('%s state does not exist in system' % state))

    def _find_country(self, country):
        if not country:
            return False
        country_id = self.env['res.country'].search([('name', '=', country)], limit=1)
        if country_id:
            return country_id.id
        else:
            raise UserError(_('%s country does not exist in system' % country))

    def _find_user(self, user):
        if not user:
            return False
        user_id = self.env['res.users'].search([('name', '=', user)], limit=1)
        if user_id:
            return user_id.id
        else:
            raise UserError(_('%s user does not exist in system' % user))

    def _find_team(self, team):
        if not team:
            return False
        team_id = self.env['crm.team'].search([('name', '=', team)], limit=1)
        if team_id:
            return team_id.id
        else:
            raise UserError(_('%s team does not exist in system' % team))

    def _find_medium(self, medium):
        if not medium:
            return False
        medium_id = self.env['utm.medium'].search([('name', '=', medium)], limit=1)
        if medium_id:
            return medium_id.id
        else:
            raise UserError(_('%s medium does not exist in system' % medium))

    def _find_source(self, source):
        if not source:
            return False
        source_id = self.env['utm.source'].search([('name', '=', source)], limit=1)
        if source_id:
            return source_id.id
        else:
            raise UserError(_('%s source does not exist in system' % source))

    def import_crm_lead(self):
        if not self.select_file:
            raise UserError(_("Please upload a file before importing."))
        file_data = base64.b64decode(self.select_file)
        if self.import_option == 'csv':
            self.import_from_csv(file_data)
        elif self.import_option == 'xls':
            self.import_from_xls(file_data)
        else:
            raise UserError(_("Invalid file format. Please upload a CSV or XLS file."))

    def import_from_csv(self, file_data):
        try:
            data = io.StringIO(file_data.decode("utf-8"))
            csv_reader = csv.reader(data, delimiter=",")
            headers = next(csv_reader, None)
            if not headers:
                raise UserError(_("CSV file is empty!"))
            for row in csv_reader:
                if len(row) < 3:
                    continue

                def get_value(val, is_number=False):
                    if is_number:
                        try:
                            return str(int(float(val))) if val else ''
                        except ValueError:
                            return ''
                    return str(val).strip() if val else ''

                name = get_value(row[0], is_number=False)
                if not name:
                    raise UserError(_("Name must be required.!"))

                self.env['crm.lead'].create({
                    'name': name,
                    'partner_id': self._find_partner(row[1]),
                    'partner_name': row[2],
                    'street': row[3],
                    'street2': row[4],
                    'city': row[5],
                    'state_id': self._find_state(row[6]),
                    'zip': row[7],
                    'country_id': self._find_country(row[8]),
                    'website': row[9],
                    'user_id': self._find_user(row[10]),
                    'team_id': self._find_team(row[11]),
                    'contact_name': row[12],
                    'email_from': row[13],
                    'function': row[14],
                    'phone': row[15],
                    'mobile': row[16],
                    'medium_id': self._find_medium(row[17]),
                    'source_id': self._find_source(row[18]),
                    'type': 'lead'
                })
        except Exception as e:
            raise UserError(_("Error processing CSV file: %s") % str(e))

    def import_from_xls(self, file_data):
        try:
            with io.BytesIO(file_data) as f:
                workbook = xlrd.open_workbook(file_contents=f.read())
                sheet = workbook.sheet_by_index(0)

                for row_idx in range(1, sheet.nrows):
                    row = sheet.row_values(row_idx)
                    if len(row) < 3:
                        continue

                    def get_value(val, is_number=False):
                        if is_number:
                            try:
                                return str(int(float(val))) if val else ''
                            except ValueError:
                                return ''
                        return str(val).strip() if val else ''

                    name = get_value(row[0], is_number=False)
                    if not name:
                        raise UserError(_("Name must be required.!"))

                    self.env['crm.lead'].create({
                        'name': name,
                        'partner_id': self._find_partner(row[1]),
                        'partner_name': row[2],
                        'street': row[3],
                        'street2': row[4],
                        'city': row[5],
                        'state_id': self._find_state(row[6]),
                        'zip': row[7],
                        'country_id': self._find_country(row[8]),
                        'website': row[9],
                        'user_id': self._find_user(row[10]),
                        'team_id': self._find_team(row[11]),
                        'contact_name': row[12],
                        'email_from': row[13],
                        'function': row[14],
                        'phone': row[15],
                        'mobile': row[16],
                        'medium_id': self._find_medium(row[17]),
                        'source_id': self._find_source(row[18]),
                        'type': 'lead'
                    })
        except Exception as e:
            raise UserError(_("Error processing XLS file: %s") % str(e))
