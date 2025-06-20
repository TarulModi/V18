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


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def action_apply_inventory(self):
        quants = self
        log_val, product_list = self._prepare_product_details_list(quants)
        print("-----log_val-----log_val----------",log_val)
        print("-----product_list-----product_list----------",product_list)

        res = super(StockQuant, self).action_apply_inventory()

        if product_list:
            self._create_quant_update_qty_log(log_val, product_list)
        return res


    def _prepare_product_details_list(self, quants):
        log_val = []
        product_list = []
        print("------quants--sfsafsafsadsadsadsadsadasdsadasdasdad---------",quants)
        for quant in quants:
            product_list.append(quant.product_id)
            log_val.append({
                'product_id': quant.product_id,
                'order_qty': quant.inventory_diff_quantity,
                'stock_quant_id': quant.id,
            })
        return log_val, product_list

    def _create_quant_update_qty_log(self, log_val, product_list):
        data_chunk = self.env['update.qty.log']._prepare_qty_data(product_list)
        self.env['update.qty.log']._push_qty_to_listing_mirror(data_chunk,
                                                               integration_name="Inventory Adjustment Created")

        for entry in data_chunk:
            for record in log_val:
                if record['product_id'].default_code == entry['sku']:
                    self.env['update.qty.log'].create({
                        'name': 'Inventory Adjustment Created',
                        'origin': 'Inventory Adjustment ' + str(record.get('product_id').name),
                        'stock_quant_id': record.get('stock_quant_id'),
                        'qty': record.get('order_qty'),
                        'pushed_qty': entry.get('quantity'),
                        'product_id': record.get('product_id').id if record.get('product_id') else False,
                    })
