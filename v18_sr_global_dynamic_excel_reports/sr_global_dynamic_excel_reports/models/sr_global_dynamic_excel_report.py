# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo.exceptions import UserError
from odoo import fields, models, api, _


class srParentObjectFields(models.Model):
    _name = "sr.parent.object.fields"
    _description = "Parent Object Fields"
    
    global_dynamic_excel_report_id = fields.Many2one('sr.global.dynamic.excel.report', string='Global Dynamic Excel Report')
    field_id = fields.Many2one('ir.model.fields', string='Fields Name', required=True, ondelete='cascade')
    label = fields.Char('Label')

    @api.onchange('field_id')
    def onchnage_field_id(self):
        if self.field_id:
            self.label = self.field_id.field_description
        return


class srChildObjectFields(models.Model):
    _name = "sr.child.object.fields"
    _description = "Child Object Fields"
    
    global_dynamic_excel_report_id = fields.Many2one('sr.global.dynamic.excel.report', string='Global Dynamic Excel Report')
    field_id = fields.Many2one('ir.model.fields', string='Fields Name', required=True, ondelete='cascade')
    label = fields.Char('Label')

    @api.onchange('field_id')
    def onchnage_field_id(self):
        if self.field_id:
            self.label = self.field_id.field_description
        return


class srGlobalDynamicExcelReport(models.Model):
    _name = 'sr.global.dynamic.excel.report'
    _description = "Global Dynamic Excel Report"
    
    name = fields.Char(string="Name", required=True)
    object_id = fields.Many2one('ir.model', string="Parent Object", required=True, ondelete='cascade')
    child_object_id = fields.Many2one('ir.model', string="Child Object")
    groupby_parent_field_id = fields.Many2one('ir.model.fields', string="Group By For parent Object")
    template_id = fields.Many2one('sr.report.template.configuration', string="Template", required=True)
    parent_object_field_ids = fields.One2many('sr.parent.object.fields', 'global_dynamic_excel_report_id', string='Parent Object Fields')
    child_object_field_ids = fields.One2many('sr.child.object.fields', 'global_dynamic_excel_report_id', string='Child Object Fields')
    act_window_ref = fields.Many2one('ir.actions.act_window', 'Window Action Reference', readonly=True, copy=False)

    def show_print_report(self):
        object_id = self.object_id.model
        view_id = self.env['ir.model.data']._xmlid_to_res_id('sr_global_dynamic_excel_reports.sr_global_dynamic_excel_report_wizard')
        action_name = _('Print (%s)') % self.name
        action_id = self.env['ir.actions.act_window'].sudo().create({
             'name': action_name,
             'type': 'ir.actions.act_window',
             'res_model': 'sr.global.excel.report.wizard',
            'context': "{'dynamic_report_id' : %d}" % (self.id),
             'view_mode':'form',
             'view_id': view_id,
             'target': 'new',
             'binding_model_id': self.object_id.id,
        })
        self.write({
            'act_window_ref': action_id.id,
        })
        return True
    
    def remove_print_report(self):
        try:
            if self.act_window_ref:
                self.act_window_ref.sudo().unlink()
        except Exception :
            raise UserError('Something went wrong while delete the action..!')
        return
