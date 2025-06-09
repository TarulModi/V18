# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################
from odoo import fields, api, models, _


class SalesOrder(models.Model):
    _inherit = 'sale.order'

    po_count = fields.Integer(string='Number of Purchase Orders', compute='_compute_po_count')
    has_consu_product = fields.Boolean("Has consumable product", default=False, compute='_compute_has_consu_product')

    @api.depends('order_line.prod_type')
    def _compute_has_consu_product(self):
        for order in self:
            order.has_consu_product = any(line.prod_type == 'non_stockable' for line in order.order_line)

    @api.depends('company_id')
    def _compute_po_count(self):
        for so in self:
            po_ids = self.env['purchase.order'].sudo().search(
                [('so_id', '=', so.id), ('company_id', '=', so.company_id.id)])
            so.po_count = len(po_ids)

    def action_confirm(self):
        mail_template_id = self.env.ref('sr_sale_customization.email_template_insufficient_stock')
        user_ids = self.env.company.insufficient_stock_email_user_ids - self.env.user
        not_stock = False
        if user_ids and mail_template_id:
            not_stock = self.order_line.filtered(
                lambda l: l.product_id and l.product_id.is_storable and l.product_uom_qty > l.free_qty_today)
            if not_stock:
                mail_template_id.partner_to = user_ids.partner_id.ids
                mail_template_id.send_mail(self.id, force_send=True)
        super(SalesOrder, self).action_confirm()
        if self.picking_ids:
            for picking in self.picking_ids:
                if picking.move_ids_without_package:
                    for move in picking.move_ids_without_package:
                        move.sudo()._onchange_product_id()
        if not_stock:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'success',
                    'sticky': False,
                    'message': _("Email successfully send!"),
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }

    def _prepare_po_context(self):
        """ Prepares the context for a new quotation (purchase.order) by sharing the values of common fields """
        self.ensure_one()
        po_context = {
            'default_so_id': self.id,
            'default_from_so': True,
            'default_company_id': self.company_id.id or self.env.company.id,
        }
        if self.user_id:
            po_context['default_user_id'] = self.user_id.id
        return po_context

    def action_create_po(self):
        action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_rfq")
        action['context'] = self._prepare_po_context()
        action['context']['search_default_po_id'] = self.id
        action.update({'view_mode': 'form',
                       'views': [(False, 'form')],
                       })
        return action

    def action_view_po(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_rfq")
        action['context'] = self._prepare_po_context()
        action['context']['search_default_draft'] = 1
        action['domain'] = [('so_id', '=', self.id)]
        po_ids = self.env['purchase.order'].sudo().search(
            [('so_id', '=', self.id), ('company_id', '=', self.company_id.id)])
        if len(po_ids) == 1:
            action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = po_ids.id
        return action


class SalesOrderLine(models.Model):
    _inherit = 'sale.order.line'

    prod_type = fields.Selection([('stockable', 'Stockable'),
                                  ('non_stockable', 'Non-stockable'),
                                  ('service', 'Service')], string='Product Type')

    def original_compute_price_unit(self):
        for line in self:
            # Don't compute the price for deleted lines.
            if not line.order_id:
                continue
            # check if the price has been manually set or there is already invoiced amount.
            # if so, the price shouldn't change as it might have been manually edited.
            if (
                    (line.technical_price_unit != line.price_unit and not line.env.context.get(
                        'force_price_recomputation'))
                    or line.qty_invoiced > 0
                    or (line.product_id.expense_policy == 'cost' and line.is_expense)
            ):
                continue
            line = line.with_context(sale_write_from_compute=True)
            if not line.product_uom or not line.product_id:
                line.price_unit = 0.0
                line.technical_price_unit = 0.0
            else:
                line = line.with_company(line.company_id)
                price = line._get_display_price()
                line.price_unit = line.product_id._get_tax_included_unit_price_from_price(
                    price,
                    product_taxes=line.product_id.taxes_id.filtered(
                        lambda tax: tax.company_id == line.env.company
                    ),
                    fiscal_position=line.order_id.fiscal_position_id,
                )
                line.technical_price_unit = line.price_unit

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        for line in self:
            # Don't compute the price for deleted lines.
            if not line.order_id:
                continue

            so_id = self.env['sale.order'].sudo().search([
                ('partner_id', '=', line.order_id.partner_id.id),
                ('state', '=', 'sale'),
                ('id', '!=', line.order_id.id)
            ], order='date_order desc', limit=1)
            # Check if a previous order exists
            if so_id:
                matching_line = so_id.order_line.filtered(lambda l: l.product_id == line.product_id)
                if matching_line:
                    previous_price = matching_line[0].price_unit  # Fetch price_unit of the first matching line
                    line.price_unit = previous_price
                    line.technical_price_unit = line.price_unit
                else:
                    line.original_compute_price_unit()
            else:
                line.original_compute_price_unit()

    @api.onchange('product_template_id')
    def _onchange_product_template_id(self):
        for res in self:
            if res.product_template_id:
                if res.product_template_id.type == 'consu' and res.product_template_id.is_storable:
                    res.prod_type = 'stockable'
                if res.product_template_id.type == 'consu' and not res.product_template_id.is_storable:
                    res.prod_type = 'non_stockable'
                if res.product_template_id.type == 'service':
                    res.prod_type = 'service'

    def _prepare_order_line_values(self):
        """ Give the values to create the corresponding order line.

        :return: `purchase.order.line` create values
        :rtype: dict
        """
        self.ensure_one()
        if self.prod_type == 'non_stockable':
            vals = {
                'product_id': self.product_id.id,
                'product_qty': self.product_uom_qty,
                'price_unit': self.price_unit,
                'sale_line_id': self.id
            }
            if self.name:
                vals['name'] = self.name
            return vals
