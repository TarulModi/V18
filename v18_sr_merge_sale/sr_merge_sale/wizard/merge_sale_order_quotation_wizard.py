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
from odoo.exceptions import ValidationError


class srMergeSaleOrdersWizard(models.TransientModel):
    _name = "merge.sale.orders.wizard"
    _description = "Merge Sale Orders Wizard"

    def _get_merge_options(self):
        option_list = [
            ("new_cancel_selected", "New SaleOrder and Cancel Selected"),
            (
                "new_delete_all_selected",
                "New SaleOrder and Delete all Selected SaleOrder",
            ),
            (
                "merge_selected_cancel_other",
                "Merge SaleOrder on existing selected SaleOrder and Cancel Others",
            ),
            (
                "merge_selected_delete_other",
                "Merge SaleOrder on existing selected SaleOrder and delete others",
            ),
        ]
        return option_list

    merge_options = fields.Selection(
        _get_merge_options, string="Merge Option", default="new_cancel_selected"
    )
    sale_ids = fields.Many2many("sale.order",
        string="Merge with",
    )
    sale_id = fields.Many2one(
        comodel_name="sale.order",
        string="Merge with",
        domain="[('id', 'in', sale_ids)]"
    )

    @api.onchange('merge_options')
    def onchange_sale_id(self):
        active_ids = self._context.get('active_ids', [])
        self.sale_ids = [(6,0,[v for v in active_ids])]

    def action_cancel(self, invoices):
        invoices.write({"state": "cancel"})

    def create_quotation(self):
        sale_ids = self.env[self.env.context.get("active_model")].browse(
            self.env.context.get("active_ids")
        )
        sale_id = self.env[self.env.context.get("active_model")].browse(
            self.env.context.get("active_id")
        )
        val_list = []
        if self.sale_id:
            for record in sale_ids:
                for line in record.order_line.filtered(
                    lambda l: l.id not in self.sale_id.order_line.ids
                ):
                    val_list.append(
                        (
                            0,
                            0,
                            {
                                "product_id": line.product_id.id,
                                "name": line.name,
                                "currency_id": line.currency_id.id,
                                "product_uom_qty": line.product_uom_qty,
                                "price_unit": line.price_unit,
                                "tax_id": [(6, 0, line.tax_id.ids)],
                            },
                        )
                    )
            self.sale_id.write(
                {
                    "order_line": val_list,
                }
            )
        else:
            for record in sale_ids:
                for line in record.order_line:
                    val_list.append(
                        (
                            0,
                            0,
                            {
                                "product_id": line.product_id.id,
                                "name": line.name,
                                "currency_id": line.currency_id.id,
                                "product_uom_qty": line.product_uom_qty,
                                "price_unit": line.price_unit,
                                "tax_id": [(6, 0, line.tax_id.ids)],
                            },
                        )
                    )

            self.env["sale.order"].create(
                {
                    "partner_id": sale_id.partner_id.id,
                    "date_order": sale_id.date_order,
                    "currency_id": sale_id.currency_id.id,
                    "payment_term_id": sale_id.payment_term_id.id,
                    "user_id": self.env.uid,
                    "order_line": val_list,
                }
            )
        return

    def merge_quotation(self):
        context = self.env.context
        active_ids = context.get("active_ids", [])
        sale_ids = self.env["sale.order"].browse(active_ids)
        partners = sale_ids.mapped("partner_id.name")
        if any(record.state not in ("draft") for record in sale_ids):
            raise ValidationError(
                _("All Quotation should be in draft state! If you need to proceed.")
            )

        if not all(name == partners[0] for name in partners):
            raise ValidationError(
                _("All partner must be same ! if you need to proceed. ")
            )

        if self.merge_options == "new_cancel_selected":
            self.create_quotation()
            self.action_cancel(sale_ids)
        elif self.merge_options == "new_delete_all_selected":
            self.create_quotation()
            sale_ids.unlink()
        elif self.merge_options == "merge_selected_cancel_other":
            self.create_quotation()
            if self.sale_id:
                invoices = sale_ids - self.sale_id
                self.action_cancel(invoices)
        elif self.merge_options == "merge_selected_delete_other":
            self.create_quotation()
            if self.sale_id:
                invoices = sale_ids - self.sale_id
                invoices.unlink()