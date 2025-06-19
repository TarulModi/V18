# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, models, api, _


class IntegrationLogDetails(models.Model):
    _name = "integration.log.details"
    _description = "Integration Log Details"
    _inherit = ['mail.thread']
    _rec_name = "integration_name"
    _order = 'id desc'

    integration_name = fields.Char('Integration Name', copy=False, tracking=True)
    remark = fields.Char('Remark', copy=False, tracking=True)
    start_date = fields.Char('Start Date', copy=False, tracking=True)
    end_date = fields.Char('End Date', copy=False, tracking=True)
    count = fields.Integer('Count', copy=False, tracking=True)
    product_ids = fields.Many2many('product.product', string="Products", copy=False, tracking=True)
    sale_order_ids = fields.Many2many('sale.order', string="Sale Orders", copy=False, tracking=True)
    bom_ids = fields.Many2many('mrp.bom', string="BOM", copy=False, tracking=True)

    def open_product_view(self):
        action = self.env['ir.actions.actions']._for_xml_id('product.product_normal_action_sell')
        action['domain'] = [('id', 'in', self.product_ids.ids)]
        return action

    def open_sale_order_view(self):
        action = self.env['ir.actions.actions']._for_xml_id('sale.action_quotations_with_onboarding')
        action['domain'] = [('id', 'in', self.sale_order_ids.ids)]
        return action

    def open_bom_view(self):
        action = self.env['ir.actions.actions']._for_xml_id('mrp.mrp_bom_form_action')
        action['domain'] = [('id', 'in', self.bom_ids.ids)]
        return action