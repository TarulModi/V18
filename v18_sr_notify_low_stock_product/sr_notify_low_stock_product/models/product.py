# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import api, fields, models, _
import json


class ProductProduct(models.Model):
    _inherit = "product.product"

    min_qty = fields.Float(string="Min Qty")
    min_qty_visible = fields.Boolean(compute="_compute_min_qty_visible")

    def _compute_min_qty_visible(self):
        for prodcut in self:
            if self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.apply_min_qty_on') == 'product':
                prodcut.min_qty_visible = True
            else:
                prodcut.min_qty_visible = False

    def send_min_qty_notification(self):
        apply_min_qty_on = self.env['ir.config_parameter'].sudo().get_param(
            'sr_notify_low_stock_product.apply_min_qty_on')

        company_ids = self.env['res.company'].sudo().search([])
        products = False
        if apply_min_qty_on == 'global':
            min_qty = float(self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.min_qty'))
            products = self.search([]).filtered(lambda x: x.qty_available < min_qty)
        if apply_min_qty_on == 'product':
            products = self.search([]).filtered(lambda x: x.qty_available < x.min_qty)
        if apply_min_qty_on == 'category':
            products = self.search([]).filtered(lambda x: x.qty_available < x.categ_id.min_qty)
        if apply_min_qty_on == 'reorder_rule':
            products = self.search([]).filtered(lambda x: x.qty_available < x.reordering_min_qty)

        if products and company_ids:
            for company in company_ids:
                template_id = self.env.ref(
                    'sr_notify_low_stock_product.email_template_min_qty_notification').id
                template = self.env['mail.template'].browse(template_id)
                values = {}
                msg = '<p style="margin: 0px; padding: 0px; font-size: 13px;"> Here is your Products which are Reached at minimum Quantity'
                if apply_min_qty_on == 'global':
                    msg += '(Global)'
                if apply_min_qty_on == 'product':
                    msg += '(Individual Product)'
                if apply_min_qty_on == 'category':
                    msg += '(Category)'
                if apply_min_qty_on == 'reorder_rule':
                    msg += '(Reordering Rule)'

                msg += ':<table style="border: 1px solid black;"><tbody><tr><th style="width:135px;background-color:#D3D3D3;border: 1px solid black;">Product</th><th style = "width: 85px;background-color:#D3D3D3;border: 1px solid black;"> Min Qty </th>'

                msg += '<th style="width: 125px;background-color:#D3D3D3;border: 1px solid black;">On hand Qty</th>'
                msg += '<th style="width: 125px;background-color:#D3D3D3;border: 1px solid black;">company</th></tr>'
                for product in products:
                    warehouse_ids = self.env['stock.warehouse'].search([('company_id', '=', company.id)])
                    location_ids = warehouse_ids.mapped('lot_stock_id')
                    quant_ids = products.stock_quant_ids.filtered(lambda r: r.location_id.id in location_ids.ids and r.company_id.id == company.id)
                    product_stock_id = quant_ids.filtered(lambda r: r.product_id.id == product.id)
                    msg += '<tr><td style="border: 1px solid black;">' + product.name + ' </td><td style="border: 1px solid black;">'
                    if apply_min_qty_on == 'global':
                        msg += str(float(
                            self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.min_qty')))
                    if apply_min_qty_on == 'product':
                        msg += str(product.min_qty)
                    if apply_min_qty_on == 'category':
                        msg += str(product.categ_id.min_qty)
                    if apply_min_qty_on == 'reorder_rule':
                        msg += str(product.reordering_min_qty)
                    msg += '</td><td style="border: 1px solid black;">' + str(
                        product_stock_id.quantity) + ' </td>'
                    msg += '</td><td style="border: 1px solid black;">' + str(
                        company.name) + ' </td></tr>'
                msg += "</tbody></table/>"
                values['subject'] = template.subject
                values['body_html'] = msg
                if self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.notify_to') == 'users':
                    if self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.min_qty_user_ids'):
                        user_ids = self.env['res.users'].browse(json.loads(
                            self.env['ir.config_parameter'].sudo().get_param(
                                'sr_notify_low_stock_product.min_qty_user_ids')))
                        emails = set(r.email for r in user_ids if r.email)
                        values['email_to'] = ','.join(emails)
                if self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.notify_to') == 'groups':
                    if self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.min_qty_group_ids'):
                        group_ids = self.env['res.groups'].browse(json.loads(
                            self.env['ir.config_parameter'].sudo().get_param(
                                'sr_notify_low_stock_product.min_qty_group_ids')))
                        user_ids = group_ids.mapped('users')
                        emails = set(r.email for r in user_ids if r.email)
                        values['email_to'] = ','.join(emails)
                if self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.outgoing_mail_id'):
                    server_id = self.env['ir.mail_server'].browse(int(
                        self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.outgoing_mail_id')))
                    values['mail_server_id'] = server_id.id
                    values['email_from'] = server_id.smtp_user
                email = self.env['mail.mail'].create(values)
                email.send()


class ProductCategory(models.Model):
    _inherit = "product.category"

    min_qty = fields.Float(string="Min Qty")
    min_qty_visible = fields.Boolean(compute="_compute_min_qty_visible")

    def _compute_min_qty_visible(self):
        for prodcut in self:
            if self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.apply_min_qty_on') == 'category':
                prodcut.min_qty_visible = True
            else:
                prodcut.min_qty_visible = False