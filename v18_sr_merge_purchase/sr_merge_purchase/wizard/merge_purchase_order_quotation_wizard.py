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


class srMergePurchaseOrdersWizard(models.TransientModel):
    _name = "merge.purchase.orders.wizard"
    _description = "Merge Purchase Orders Wizard"

    @api.model
    def default_get(self, fields):
        res = super(srMergePurchaseOrdersWizard, self).default_get(fields)
        if self.env.user.has_groups("base.group_multi_currency"):
            res["group_multi_currency"] = True
        return res

    def _get_merge_options(self):
        option_list = [
            ("new_cancel_selected", "New RFQ and Cancel Selected"),
            (
                "new_delete_all_selected",
                "New RFQ and Delete all Selected RFQ",
            ),
            (
                "merge_selected_cancel_other",
                "Merge RFQ on existing selected RFQ and Cancel Others",
            ),
            (
                "merge_selected_delete_other",
                "Merge RFQ on existing selected RFQ and delete others",
            ),
        ]
        return option_list

    merge_options = fields.Selection(
        _get_merge_options, string="Merge Option", default="new_cancel_selected"
    )
    merge_multi_currency_purchase = fields.Boolean(string="Merge multi currency Purchase")
    currency_id = fields.Many2one(comodel_name="res.currency", string="Select Currency")
    purchase_ids = fields.Many2many("purchase.order")
    purchase_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Merge with",
        domain="[('id', 'in', purchase_ids)]",
    )
    group_multi_currency = fields.Boolean(string="Multi Currency")

    @api.onchange('merge_options')
    def onchange_purchase_id(self):
        active_ids = self._context.get('active_ids', [])
        self.purchase_ids = [(6,0,[v for v in active_ids])]

    def action_cancel(self, invoices):
        invoices.write({"state": "cancel"})

    def create_quotation(self):
        purchase_ids = self.env[self.env.context.get("active_model")].browse(
            self.env.context.get("active_ids")
        )
        purchase_id = self.env[self.env.context.get("active_model")].browse(
            self.env.context.get("active_id")
        )
        val_list = []
        if self.purchase_id:
            currency_id = (
                self.currency_id
                if self.merge_multi_currency_purchase and self.currency_id
                else self.purchase_id.currency_id
            )
            for record in purchase_ids:
                for line in record.order_line.filtered(
                    lambda l: l.id not in self.purchase_id.order_line.ids
                ):
                    price_unit = self.purchase_id.currency_id._convert(line.price_unit, currency_id, line.company_id, line.date_order or fields.Date.today())
                    val_list.append(
                        (
                            0,
                            0,
                            {
                                "product_id": line.product_id.id,
                                "name": line.name,
                                "currency_id": currency_id.id,
                                "product_uom_qty": line.product_uom_qty,
                                "product_qty": line.product_uom_qty,
                                "price_unit": price_unit,
                                "taxes_id": [(6, 0, line.taxes_id.ids)],
                            },
                        )
                    )

            if self.merge_multi_currency_purchase and self.currency_id:
                self.purchase_id.write({"currency_id": self.currency_id.id})

            self.purchase_id.write(
                {
                    "order_line": val_list,
                }
            )
        else:
            for record in purchase_ids:
                for line in record.order_line:
                    currency_id = (
                        self.currency_id
                        if self.merge_multi_currency_purchase and self.currency_id
                        else line.currency_id
                    )
                    price_unit = line.currency_id._convert(line.price_unit, currency_id, line.company_id, line.date_order or fields.Date.today())
                    val_list.append(
                        (
                            0,
                            0,
                            {
                                "product_id": line.product_id.id,
                                "name": line.name,
                                "currency_id": currency_id.id,
                                "product_uom_qty": line.product_uom_qty,
                                "product_qty": line.product_uom_qty,
                                "price_unit": price_unit,
                                "taxes_id": [(6, 0, line.taxes_id.ids)],
                            },
                        )
                    )

            currency_id = (
                self.currency_id
                if self.merge_multi_currency_purchase and self.currency_id
                else purchase_id.currency_id
            )
            self.env["purchase.order"].create(
                {
                    "partner_id": purchase_id.partner_id.id,
                    "date_approve": purchase_id.date_approve,
                    "date_planned": purchase_id.date_planned,
                    "currency_id": currency_id.id,
                    "payment_term_id": purchase_id.payment_term_id.id,
                    "user_id": self.env.uid,
                    "order_line": val_list,
                }
            )
        return

    def merge_quotation(self):
        context = self.env.context
        active_ids = context.get("active_ids", [])
        purchase_ids = self.env["purchase.order"].browse(active_ids)
        partners = purchase_ids.mapped("partner_id.name")
        if len(purchase_ids.ids) < 1:
            raise ValidationError(
                _("Please select atleast two quotation to perform merge operation.")
            )

        if any(record.state not in ("draft") for record in purchase_ids):
            raise ValidationError(
                _("All Quotation should be in draft state! If you need to proceed.")
            )

        if not all(name == partners[0] for name in partners):
            raise ValidationError(
                _("All partner must be same ! if you need to proceed. ")
            )

        if self.merge_options == "new_cancel_selected":
            self.create_quotation()
            self.action_cancel(purchase_ids)
        elif self.merge_options == "new_delete_all_selected":
            self.create_quotation()
            purchase_ids.button_cancel()
            purchase_ids.unlink()
        elif self.merge_options == "merge_selected_cancel_other":
            self.create_quotation()
            if self.purchase_id:
                invoices = purchase_ids - self.purchase_id
                self.action_cancel(invoices)
        elif self.merge_options == "merge_selected_delete_other":
            self.create_quotation()
            if self.purchase_id:
                invoices = purchase_ids - self.purchase_id
                invoices.button_cancel()
                invoices.unlink()
