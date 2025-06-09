# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models,fields,api,_

class FinancialStatementNotes(models.Model):
    _name = 'financial.statement.notes'
    _description = 'Financial Statement Notes'
    _rec_name = 'name'

    name = fields.Char(default="Financial Statement Notes")
    property_plant_equipment_ids = fields.Many2many('account.account','financial_statement_notes_ppe_rel','financial_statement_id','account_id',string='Property Plant Equipments')
    wip_ids = fields.Many2many('account.account','financial_statement_notes_wip_rel','financial_statement_id','account_id',string='Work In Progress')
    cash_equivalents_ids = fields.Many2many('account.account','financial_statement_notes_ppene_rel','financial_statement_id','account_id',string='Cash And Cash Equivalents')
    related_party_ids = fields.Many2many('account.account','financial_statement_notes_related_party_rel','financial_statement_id','account_id',string='Related Party')
    employee_provision_ids = fields.Many2many('account.account','financial_statement_notes_employee_provision_rel','financial_statement_id','account_id',string='Provisions For Employee')

    financial_line_ids = fields.One2many('financial.statement.notes.line','financial_id')
