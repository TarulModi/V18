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
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        if self.order_line:
            message = "You can not confirm this order because of following reasons:"
            is_warning = False
            for line in self.order_line:
                if line.is_stock_available:
                    is_warning = True
                    message += _('\n\nYou have added %s %s of %s but you only have %s %s available in %s warehouse.') % \
                               (line.product_uom_qty,
                                line.product_uom.name,
                                line.product_id.name,
                                line.product_id.with_context(
                    {'warehouse': line.order_id.warehouse_id.id}).qty_available,
                                line.product_uom.name,
                                line.order_id.warehouse_id.name)
            if is_warning:
                raise ValidationError(message)
        super(SaleOrder, self)._action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id', 'product_uom_qty')
    def check_on_hand_qty(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        restrict_configuration = ICPSudo.get_param('restrict_product_stock_in_sale_setting')
        for line in self:
            if restrict_configuration:
                available_product_qty = line.product_id.with_context(
                    {'warehouse': line.order_id.warehouse_id.id}).qty_available
                if line.product_uom_qty > available_product_qty:
                    line.is_stock_available = True
                else:
                    line.is_stock_available = False
            else:
                line.is_stock_available = False

    is_stock_available = fields.Boolean(string="Is Stock Available?",compute="check_on_hand_qty")
