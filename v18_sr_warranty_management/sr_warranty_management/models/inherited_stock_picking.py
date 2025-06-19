# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        result = super(StockPicking, self).button_validate()
        for record in self:
            if record.return_id:
                return result
            if record.sale_id and record.state == 'done':
                record.sale_id.create_warranty_records(record.sale_id)
            if record.move_ids_without_package:
                for line in record.move_ids_without_package:
                    warranty_id = self.env["sr.product.warranty"].search(
                        [
                            ("product_id", "=", line.product_tmpl_id.id),
                            ("sale_order_id", "=", record.origin),
                        ]
                    )
                    if warranty_id:
                        for lot in line.lot_ids:
                            warranty_id.serial_number = lot.name
        return result
