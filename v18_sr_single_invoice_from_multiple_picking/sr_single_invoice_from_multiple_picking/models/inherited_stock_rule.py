# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields


class StockRule(models.Model):
    _inherit = 'stock.rule'
    
    created_sale_order_line_id = fields.Many2one('sale.order.line', string="order line")
    
    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        move_values = super(StockRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, company_id, values)
        move_values.update({
                'created_sale_order_line_id':values.get('sale_line_id'),
            })
        return move_values 
