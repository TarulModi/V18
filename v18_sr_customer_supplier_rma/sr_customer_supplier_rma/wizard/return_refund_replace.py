# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ReturnRefundReplace(models.TransientModel):
    _name = 'return.refund.replace'
    _description = 'Return Refund Replace'

    line_ids = fields.One2many("return.refund.replace.line", 'return_refund_id')
    replace_line_ids = fields.One2many("return.replace.line", 'return_refund_id')

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        if self.env.context.get('active_id'):
            rma_order_id = self.env['rma.order'].browse([self.env.context.get('active_id')]).exists()
            if rma_order_id and rma_order_id.rma_order_line_ids:
                line_lst = []
                for line in rma_order_id.rma_order_line_ids:
                    line_lst.append((0, 0, {
                        'product_id' : line.product_id.id,
                        'delivery_qty' : line.delivery_qty,
                        'return_id' : line.return_id.id,
                        'reject_id' : line.reject_id.id,
                        'return_qty' : line.return_qty,
                        'rma_order_line_id': line.id,
                        'sale_line_id': line.sale_line_id.id,
                    }))

                defaults['line_ids'] = line_lst
            if rma_order_id and rma_order_id.rma_replaced_product_ids:
                line_replace_lst = []
                for line in rma_order_id.rma_replaced_product_ids:
                    line_replace_lst.append((0, 0, {
                        'rma_order_id': line.rma_order_id.id,
                        'rma_replaced_product_id' : line.id,
                        'product_id' : line.product_id.id,
                        'qty' : line.qty,
                        'price': line.price,
                    }))
                defaults['replace_line_ids'] = line_replace_lst
        return defaults

    def button_submit(self):
        if not all(line.return_id or line.reject_id for line in self.line_ids):
            raise ValidationError(
                _("Please select the return/no return and reject for entered returned qty to proceed"))

        if not all(line.return_qty > 0 for line in self.line_ids):
            raise ValidationError(_("Please select at least one return item to proceed"))

        if self.replace_line_ids and not all(line.qty > 0 for line in self.replace_line_ids):
            raise ValidationError(_("Please select at least one replace quantity item to proceed"))

        for line in self.line_ids:
            if line.return_qty > line.delivery_qty:
                raise ValidationError(
                    _("Return quantity for product '%s' cannot exceed delivered quantity (Delivered: %s, Return: %s).") % (
                        line.product_id.display_name, line.delivery_qty, line.return_qty
                    )
                )

        if self.env.context.get('active_id'):
            rma_order_id = self.env['rma.order'].browse([self.env.context.get('active_id')]).exists()
            if rma_order_id and self.line_ids:
                for line in self.line_ids:
                    line.rma_order_line_id.write({
                        'return_id' : line.return_id.id,
                        'reject_id' : line.reject_id.id,
                        'return_qty' : line.return_qty
                    })
            if rma_order_id and self.replace_line_ids:
                replace_list = []
                for line in self.replace_line_ids:
                    if line.rma_replaced_product_id:
                        line.rma_replaced_product_id.write({
                            'product_id': line.product_id.id,
                            'qty': line.qty,
                            'price': line.price
                        })
                    else:
                        replace_list.append((0, 0, {
                            'product_id' : line.product_id.id,
                            'qty' : line.qty,
                            'price' : line.price
                        }))

                if replace_list:
                    rma_order_id.rma_replaced_product_ids = replace_list


class ReturnRefundReplaceLine(models.TransientModel):
    _name = 'return.refund.replace.line'
    _description = 'Return Refund Replace Line'

    return_refund_id = fields.Many2one('return.refund.replace')
    rma_order_line_id = fields.Many2one('rma.order.line')
    product_id = fields.Many2one('product.product', string="Product")
    return_id = fields.Many2one('return.no.return', string="Return/NoReturn")
    reject_id = fields.Many2one('reject.reason', string="Reject Reason")
    delivery_qty = fields.Float('Delivery QTY')
    pending_qty = fields.Float('Pending QTY')
    return_qty = fields.Float('Return QTY')
    sale_line_id = fields.Many2one('sale.order.line', string="Sale Order Line")


class ReturnReplaceLine(models.TransientModel):
    _name = 'return.replace.line'
    _description = 'Return Replace Line'

    return_refund_id = fields.Many2one('return.refund.replace')
    rma_replaced_product_id = fields.Many2one('rma.replaced.product')
    rma_order_id = fields.Many2one('rma.order')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    qty = fields.Float('QTY')
    price = fields.Float('Price')

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.price = self.product_id.lst_price
