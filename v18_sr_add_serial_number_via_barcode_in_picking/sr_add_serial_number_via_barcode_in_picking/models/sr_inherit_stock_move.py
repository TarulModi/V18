# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError


class srStockMove(models.Model):
    _inherit = 'stock.move'
    
    barcode = fields.Char(string="Barcode")

    @api.onchange('barcode')
    def onchange_barcode(self):
        counter = 0
        for move_line in self.move_line_ids:
            if self.picking_id.picking_type_id.code == 'outgoing':
                stock_production_lot_ids = self.env['stock.lot'].search([('name', '=', self.barcode)])
                if stock_production_lot_ids:
                    for stock_production_lot_id in stock_production_lot_ids:
                        if stock_production_lot_id.product_id.id != self.product_id.id:
                            raise UserError(_('You have scanned lot/serial number for different product'))
                        if move_line.lot_id.id == stock_production_lot_id.id:
                            if self.product_id.tracking == 'serial':
                                move_line.write({
                                    'quantity' : 1
                                    })
                            elif self.product_id.tracking == 'lot':
                                move_line.write({
                                    'quantity' : move_line.reserved_uom_qty if stock_production_lot_id.product_qty >= move_line.reserved_uom_qty else stock_production_lot_id.product_qty
                                    })
                            break
                else:
                    raise UserError(_('%s Serial/Lot Number is not available in system') % self.barcode)
            
            if self.picking_id.picking_type_id.code == 'incoming':
                if not move_line.lot_name:
                    move_line.lot_name = self.barcode
                    move_line.quantity = 1 if self.product_id.tracking == 'serial' else move_line.reserved_uom_qty
                    break
                else:
                    counter += 1
            
            if counter == len(self.move_line_ids):
                raise UserError('All the serials/lots are assigned')
        self.barcode = False
