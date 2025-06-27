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
from collections import defaultdict

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
        products = self.env['product.product']
        all_locations = self.env['stock.location'].search([('min_qty', '>', 0)])
        if apply_min_qty_on == 'global':
            min_qty = float(self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.min_qty'))
            products = self.search([]).filtered(lambda x: x.qty_available < min_qty)
        if apply_min_qty_on == 'product':
            products = self.search([]).filtered(lambda x: x.qty_available < x.min_qty)
        if apply_min_qty_on == 'category':
            products = self.search([]).filtered(lambda x: x.qty_available < x.categ_id.min_qty)
        if apply_min_qty_on == 'reorder_rule':
            products = self.search([]).filtered(lambda x: x.qty_available < x.reordering_min_qty)
        if apply_min_qty_on == 'location':
            products = self.env['product.product']
            StockQuant = self.env['stock.quant']
            for location in all_locations:
                loc_min_qty = location.min_qty
                if loc_min_qty <= 0:
                    continue
                quants = StockQuant.search([
                    ('location_id', '=', location.id),
                    ('quantity', '<', loc_min_qty),
                ])
                for quant in quants:
                    if quant.product_id not in products:
                        products |= quant.product_id

            print('products--------------',products)
            print('all_locations---------',all_locations)

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
                if apply_min_qty_on == 'location':
                    msg += '(location)'

                msg += ':<table style="border: 1px solid black;"><tbody><tr><th style="width:135px;background-color:#D3D3D3;border: 1px solid black;">Product</th><th style = "width: 85px;background-color:#D3D3D3;border: 1px solid black;"> Min Qty </th>'

                msg += '<th style="width: 125px;background-color:#D3D3D3;border: 1px solid black;">On hand Qty</th>'
                msg += '<th style="width: 125px;background-color:#D3D3D3;border: 1px solid black;">company</th></tr>'
                for product in products:
                    warehouse_ids = self.env['stock.warehouse'].search([('company_id', '=', company.id)])
                    location_ids = warehouse_ids.mapped('lot_stock_id')
                    quant_ids = products.stock_quant_ids.filtered(
                        lambda r: r.location_id.id in location_ids.ids and r.company_id.id == company.id)
                    product_stock_id = quant_ids.filtered(lambda r: r.product_id.id == product.id)
                    products = products.filtered(lambda p: p.company_id.id == company.id or not p.company_id)
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
                    if apply_min_qty_on == 'location':
                        location_min_qty = 0
                        StockQuant = self.env['stock.quant']
                        for location in all_locations:
                            loc_min_qty = location.min_qty
                            if loc_min_qty <= 0:
                                continue
                            quant = StockQuant.search([
                                ('location_id', '=', location.id),
                                ('product_id', '=', product.id),
                                ('quantity', '<', loc_min_qty)
                            ], limit=1)
                            if quant:
                                location_min_qty = loc_min_qty
                                break
                        msg += str(location_min_qty)

                    msg += '</td><td style="border: 1px solid black;">' + str(
                        product_stock_id.quantity) + ' </td>'
                    msg += '</td><td style="border: 1px solid black;">' + str(
                        company.name) + ' </td></tr>'
                msg += "</tbody></table/>"
                values['subject'] = template.subject
                values['body_html'] = msg

                # -
                if apply_min_qty_on == 'location':
                    StockQuant = self.env['stock.quant'].search([('company_id', '=', company.id)])
                    user_product_map = defaultdict(set)
                    company_name = company.name
                    covered_products = set()

                    for location in all_locations:
                        loc_min_qty = location.min_qty
                        if loc_min_qty <= 0:
                            continue
                        for product in products:
                            quant = StockQuant.search([
                                ('location_id', '=', location.id),
                                ('product_id', '=', product.id),
                                ('quantity', '<', loc_min_qty)
                            ], limit=1)
                            if quant:
                                if location.user_ids:
                                    for user in location.user_ids.filtered(lambda u: u.email):
                                        user_product_map[user].add(product)
                                        covered_products.add(product)

                    for user, user_products in user_product_map.items():
                        if not user.email or not user_products:
                            continue

                        user_locations = user.location_ids if hasattr(user, 'location_ids') else self.env[
                            'stock.location'].search([('user_ids', 'in', user.id)])

                        user_msg = '<p style="margin: 0px; padding: 0px; font-size: 13px;"> Here are your Products which are below minimum quantity (Location):</p>'
                        user_msg += '<table style="border: 1px solid black;"><tbody><tr>'
                        user_msg += '<th style="width:135px;background-color:#D3D3D3;border: 1px solid black;">Product</th>'
                        user_msg += '<th style="width: 85px;background-color:#D3D3D3;border: 1px solid black;">Min Qty</th>'
                        user_msg += '<th style="width: 125px;background-color:#D3D3D3;border: 1px solid black;">On hand Qty</th>'
                        user_msg += '<th style="width: 125px;background-color:#D3D3D3;border: 1px solid black;">Company</th></tr>'

                        for product in user_products:
                            location_min_qty = 0
                            total_qty = 0
                            for location in user_locations.filtered(lambda l: l.min_qty > 0):
                                quant = StockQuant.search([
                                    ('location_id', '=', location.id),
                                    ('product_id', '=', product.id),
                                    ('quantity', '<', location.min_qty)
                                ], limit=1)
                                if quant:
                                    location_min_qty = location.min_qty
                                    break
                            for location in user_locations:
                                qty = StockQuant.search([
                                    ('location_id', '=', location.id),
                                    ('product_id', '=', product.id),
                                ]).mapped('quantity')
                                total_qty += sum(qty) if qty else 0

                            user_msg += f'<tr><td style="border: 1px solid black;">{product.name}</td>'
                            user_msg += f'<td style="border: 1px solid black;">{location_min_qty}</td>'
                            user_msg += f'<td style="border: 1px solid black;">{total_qty}</td>'
                            user_msg += f'<td style="border: 1px solid black;">{company_name}</td></tr>'

                        user_msg += "</tbody></table>"

                        user_values = values.copy()
                        user_values['email_to'] = user.email
                        user_values['body_html'] = user_msg
                        user_values['subject'] = template.subject

                        outgoing_mail_param = self.env['ir.config_parameter'].sudo().get_param(
                            'sr_notify_low_stock_product.outgoing_mail_id')
                        if outgoing_mail_param:
                            server_id = self.env['ir.mail_server'].browse(int(outgoing_mail_param))
                            user_values['mail_server_id'] = server_id.id
                            user_values['email_from'] = server_id.smtp_user

                        email = self.env['mail.mail'].create(user_values)
                        email.send()

                    remaining_products = products - self.env['product.product'].browse([p.id for p in covered_products])
                    if remaining_products:
                        notify_to = self.env['ir.config_parameter'].sudo().get_param(
                            'sr_notify_low_stock_product.notify_to')
                        emails = set()

                        if notify_to == 'users':
                            user_param = self.env['ir.config_parameter'].sudo().get_param(
                                'sr_notify_low_stock_product.min_qty_user_ids')
                            if user_param:
                                user_ids = self.env['res.users'].browse(json.loads(user_param))
                                emails.update(user.email for user in user_ids if user.email)

                        elif notify_to == 'groups':
                            group_param = self.env['ir.config_parameter'].sudo().get_param(
                                'sr_notify_low_stock_product.min_qty_group_ids')
                            if group_param:
                                group_ids = self.env['res.groups'].browse(json.loads(group_param))
                                user_ids = group_ids.mapped('users')
                                emails.update(user.email for user in user_ids if user.email)

                        if emails:
                            fallback_msg = '<p style="margin: 0px; padding: 0px; font-size: 13px;">Products below minimum quantity (locations):</p>'
                            fallback_msg += '<table style="border: 1px solid black;"><tbody><tr>'
                            fallback_msg += '<th style="width:135px;background-color:#D3D3D3;border: 1px solid black;">Product</th>'
                            fallback_msg += '<th style="width: 85px;background-color:#D3D3D3;border: 1px solid black;">Min Qty</th>'
                            fallback_msg += '<th style="width: 125px;background-color:#D3D3D3;border: 1px solid black;">On hand Qty</th>'
                            fallback_msg += '<th style="width: 125px;background-color:#D3D3D3;border: 1px solid black;">Company</th></tr>'

                            for product in remaining_products:
                                location_min_qty = 0
                                for location in all_locations.filtered(lambda l: not l.user_ids and l.min_qty > 0):
                                    quant = StockQuant.search([
                                        ('location_id', '=', location.id),
                                        ('product_id', '=', product.id),
                                        ('quantity', '<', location.min_qty)
                                    ], limit=1)
                                    if quant:
                                        location_min_qty = location.min_qty
                                        break
                                total_qty = sum(
                                    StockQuant.search([
                                        ('product_id', '=', product.id),
                                        ('location_id', 'in', all_locations.filtered(lambda l: not l.user_ids).ids)
                                    ]).mapped('quantity')
                                )

                                fallback_msg += f'<tr><td style="border: 1px solid black;">{product.name}</td>'
                                fallback_msg += f'<td style="border: 1px solid black;">{location_min_qty}</td>'
                                fallback_msg += f'<td style="border: 1px solid black;">{total_qty}</td>'
                                fallback_msg += f'<td style="border: 1px solid black;">{company_name}</td></tr>'

                            fallback_msg += "</tbody></table>"

                            fallback_values = values.copy()
                            fallback_values['email_to'] = ','.join(emails)
                            fallback_values['body_html'] = fallback_msg
                            fallback_values['subject'] = template.subject

                            if outgoing_mail_param:
                                server_id = self.env['ir.mail_server'].browse(int(outgoing_mail_param))
                                fallback_values['mail_server_id'] = server_id.id
                                fallback_values['email_from'] = server_id.smtp_user

                            email = self.env['mail.mail'].create(fallback_values)
                            email.send()
                # -
                else:
                    notify_to = self.env['ir.config_parameter'].sudo().get_param(
                        'sr_notify_low_stock_product.notify_to')
                    emails = set()

                    if notify_to == 'users':
                        user_param = self.env['ir.config_parameter'].sudo().get_param(
                            'sr_notify_low_stock_product.min_qty_user_ids')
                        if user_param:
                            user_ids = self.env['res.users'].browse(json.loads(user_param))
                            emails.update(user.email for user in user_ids if user.email)

                    if notify_to == 'groups':
                        group_param = self.env['ir.config_parameter'].sudo().get_param(
                            'sr_notify_low_stock_product.min_qty_group_ids')
                        if group_param:
                            group_ids = self.env['res.groups'].browse(json.loads(group_param))
                            user_ids = group_ids.mapped('users')
                            emails.update(user.email for user in user_ids if user.email)

                    if emails:
                        values['email_to'] = ','.join(emails)

                        outgoing_mail_param = self.env['ir.config_parameter'].sudo().get_param(
                            'sr_notify_low_stock_product.outgoing_mail_id')
                        if outgoing_mail_param:
                            server_id = self.env['ir.mail_server'].browse(int(outgoing_mail_param))
                            values['mail_server_id'] = server_id.id
                            values['email_from'] = server_id.smtp_user

                        email = self.env['mail.mail'].create(values)
                        print('----email----', email)
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