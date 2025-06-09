# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import api, models, _
from odoo.osv import expression


class srStockProductionLot(models.Model):
    _inherit = "stock.lot"

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=100, order=None):
        super(srStockProductionLot, self)._name_search(
            name=name,
            domain=domain,
            operator=operator,
            limit=limit,
            order=order,
        )
        context = self._context
        product_id = context.get("product_id")
        is_pickup = context.get("is_pickup")
        domain = domain or []
        name_domain = []
        if product_id and is_pickup:
            lot_ids = self.search([('product_id', '=', product_id)])
            line = self.env["sale.order.line"].search(
                [('lot_ids', 'in', lot_ids.ids), ('is_pickup', '=', True)]
            )
            name_domain = [
                ('id', 'not in', line.lot_ids.ids),
                ('product_id', '=', product_id),
            ]
            domain = expression.AND([name_domain, domain])
        return self._search(domain, limit=limit, order=order)
