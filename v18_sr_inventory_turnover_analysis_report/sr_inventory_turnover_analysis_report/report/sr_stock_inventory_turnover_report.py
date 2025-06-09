# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from datetime import date
from odoo import api, models


class srReportStockInventoryTurnover(models.AbstractModel):
    _name = 'report.sr_inventory_turnover_analysis_report.turnover'
    _description = "Inventory Turnover Analysis Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.inventory.turnover.report'].browse(docids)

        if docs.product_ids and docs.categ_ids:
            products = docs.product_ids.search(
                ['|', ('id', 'in', docs.product_ids.ids), ('categ_id', 'in', docs.categ_ids.ids)])
        elif docs.product_ids and not docs.categ_ids:
            products = docs.product_ids.search([('id', 'in', docs.product_ids.ids)])
        elif docs.categ_ids:
            products = docs.product_ids.search([('categ_id', 'in', docs.categ_ids.ids)])
        else:
            products = docs.product_ids.search([])

        domain = []
        if docs.warehouse_ids:
            domain.append(('warehouse_id', 'in', docs.warehouse_ids.ids))
        if docs.company_ids:
            domain.append(('company_id', 'in', docs.company_ids.ids))

        print_data = []
        for product in products:
            moves = self.env['stock.move'].search(domain+[('product_id', '=', product.id),('state', '=', 'done')])
            prod_dict={}
            prod_dict.update({'name': product.name})

            purchase_moves = moves.filtered(lambda rec: rec.location_dest_id.usage == 'internal')
            sales_moves = moves.filtered(lambda rec: rec.location_id.usage == 'internal')

            if docs.start_date and docs.end_date:
                opening_stock = sum(move.product_uom_qty for move in purchase_moves.filtered(lambda rec: rec.date.date() < docs.start_date)) - sum(
                    move.product_uom_qty for move in sales_moves.filtered(lambda rec: rec.date.date() < docs.start_date))
                closing_stock = sum(move.product_uom_qty for move in purchase_moves.filtered(
                    lambda rec: rec.date.date() > docs.start_date and rec.date.date() < docs.end_date)) - sum(
                    move.product_uom_qty for move in
                    sales_moves.filtered(lambda rec:rec.date.date() > docs.start_date and rec.date.date() < docs.end_date))
                sales = sum(move.product_uom_qty for move in sales_moves.filtered(lambda rec: rec.date.date() > docs.start_date and rec.date.date() < docs.end_date))
                purchase = sum(move.product_uom_qty for move in
                               purchase_moves.filtered(lambda rec: rec.date.date() > docs.start_date and rec.date.date() < docs.end_date))
                
            elif docs.start_date:
                opening_stock = sum(move.product_uom_qty for move in purchase_moves.filtered(lambda rec: rec.date.date() < docs.start_date)) - sum(
                    move.product_uom_qty for move in sales_moves.filtered(lambda rec: rec.date.date() < docs.start_date))
                closing_stock = sum(move.product_uom_qty for move in purchase_moves.filtered(
                    lambda rec: rec.date.date() > docs.start_date))- sum(
                    move.product_uom_qty for move in sales_moves.filtered(lambda rec: rec.date.date() > docs.start_date))
                sales = sum(move.product_uom_qty for move in sales_moves.filtered(lambda rec: rec.date.date() > docs.start_date))
                purchase = sum(move.product_uom_qty for move in
                               purchase_moves.filtered(lambda rec: rec.date.date() > docs.start_date))

            elif docs.end_date:
                opening_stock = 0
                closing_stock = sum(move.product_uom_qty for move in moves.filtered(lambda rec: rec.location_dest_id.usage == 'internal') and date < docs.end_date) - sum(
                    move.product_uom_qty for move in sales_moves.filtered(lambda rec: rec.date.date() < docs.end_date))
                sales = sum(move.product_uom_qty for move in
                            sales_moves.filtered(lambda rec: rec.date.date() < docs.end_date))
                purchase = sum(move.product_uom_qty for move in
                                purchase_moves.filtered(lambda rec: rec.date.date() < docs.end_date))
            
            else:
                opening_stock = 0
                closing_stock = sum(move.product_uom_qty for move in purchase_moves) - sum(
                    move.product_uom_qty for move in sales_moves)
                sales = sum(move.product_uom_qty for move in sales_moves)
                purchase = sum(move.product_uom_qty for move in purchase_moves)
            
            prod_dict.update({'sales': sales,
                              'purchase': purchase,
                              'opening_stock': opening_stock,
                              'closing_stock': closing_stock,
                              'average_inventory':(opening_stock+closing_stock)/2,
                              'inventory_turnover_ratio':0.00 if (opening_stock+closing_stock)/2 == 0 else (opening_stock+ purchase - closing_stock)/((opening_stock+closing_stock)/2)})
            print_data.append(prod_dict)

        return {
            'doc_ids': docids,
            'doc_model': 'stock.inventory.turnover.report',
            'docs': docs,
            'data': data,
            'print_data': print_data
        }
