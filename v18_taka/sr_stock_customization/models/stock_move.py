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


class StockMove(models.Model):
    _inherit = 'stock.move'

    prod_type = fields.Selection([('stockable', 'Stockable'),
                                  ('non_stockable', 'Non-stockable'),
                                  ('service', 'Service')], string='Product Type')

    @api.onchange('product_id', 'picking_type_id')
    def _onchange_product_id(self):
        for res in self:
            super(StockMove,self)._onchange_product_id()
            if res.product_id:
                if res.product_id.type == 'consu' and res.product_id.is_storable:
                    res.prod_type = 'stockable'
                if res.product_id.type == 'consu' and not res.product_id.is_storable:
                    res.prod_type = 'non_stockable'
                if res.product_id.type == 'service':
                    res.prod_type = 'service'