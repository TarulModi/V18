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


class StockPikcing(models.Model):
    _inherit = 'stock.picking'
    
    is_invoiced = fields.Boolean(string="Invoiced")
    
    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        move_values = super(StockPikcing, self)._get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values)
        move_values.update({
                'created_sale_order_line_id':values.get('sale_line_id'),
            })
        return move_values
