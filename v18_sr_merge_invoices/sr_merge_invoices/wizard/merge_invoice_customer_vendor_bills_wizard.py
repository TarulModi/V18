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


class srMergeCustomerInvoiceVendorBillsWizard(models.TransientModel):
    _name = "merge.inv.cust.vendor.bills.wizard"
    _description = "Merge Invoice Customer Vendor Bills Wizard"

    @api.model
    def default_get(self, fields):
        res = super(srMergeCustomerInvoiceVendorBillsWizard, self).default_get(fields)
        if self.env.user.has_groups("base.group_multi_currency"):
            res["group_multi_currency"] = True
        return res

    def _get_merge_options(self):
        option_list = [
            ("new_cancel_selected", "New Invoice/Bill and Cancel Selected"),
            (
                "new_delete_all_selected",
                "New Invoice/Bill and Delete all Selected Invoices",
            ),
            (
                "merge_selected_cancel_other",
                "Merge Invoices/Bills on existing selected Invoice/Bill and Cancel Others",
            ),
            (
                "merge_selected_delete_other",
                "Merge Invoices/Bills on existing selected Invoices/Bill and delete others",
            ),
        ]
        return option_list

    merge_options = fields.Selection(
        _get_merge_options, string="Merge Option", default="new_cancel_selected"
    )
    merge_multi_currency_inv = fields.Boolean(string="Merge Invoice in different Invoice")
    currency_id = fields.Many2one(comodel_name="res.currency", string="Select Currency")
    move_ids = fields.Many2many("account.move")
    move_id = fields.Many2one(
        comodel_name="account.move",
        string="Merge with",
        domain='[("id", "in", move_ids)]',
    )
    group_multi_currency = fields.Boolean(string="Multi Currency")

    @api.onchange('merge_options')
    def onchange_purchase_id(self):
        active_ids = self._context.get('active_ids', [])
        self.move_ids = [(6,0,[v for v in active_ids])]
        if self.merge_options in ['new_cancel_selected', 'new_delete_all_selected']:
            self.move_id = False

    def invoice_cancel(self, invoices):
        invoices.write({"state": "cancel"})

    def create_invoice(self):
        invoice_ids = self.env[self.env.context.get("active_model")].browse(
            self.env.context.get("active_ids")
        )
        invoice = self.env[self.env.context.get("active_model")].browse(
            self.env.context.get("active_id")
        )
        val_list = []
        if self.move_id:
            currency_id = (
                self.currency_id
                if self.merge_multi_currency_inv and self.currency_id
                else self.move_id.currency_id
            )
            for line in self.move_id.invoice_line_ids:
                price_unit = self.move_id.currency_id._convert(line.price_unit, currency_id, line.company_id, line.invoice_date or fields.Date.today())
                val_list.append(
                    (
                        0,
                        0,
                        {
                            "product_id": line.product_id.id,
                            "name": line.name,
                            "currency_id": currency_id.id,
                            "account_id": line.account_id.id,
                            "quantity": line.quantity,
                            "price_unit": price_unit,
                            "tax_ids": [(6, 0, line.tax_ids.ids)],
                        },
                    )
                )

            for record in invoice_ids:
                for move in record.invoice_line_ids.filtered(
                    lambda l: l.id not in self.move_id.invoice_line_ids.ids
                ):
                    price_unit = self.move_id.currency_id._convert(move.price_unit, currency_id, move.company_id, move.invoice_date or fields.Date.today())
                    val_list.append(
                        (
                            0,
                            0,
                            {
                                "product_id": move.product_id.id,
                                "name": move.name,
                                "currency_id": currency_id.id,
                                "account_id": move.account_id.id,
                                "quantity": move.quantity,
                                "price_unit": price_unit,
                                "tax_ids": [(6, 0, move.tax_ids.ids)],
                            },
                        )
                    )

            if self.merge_multi_currency_inv and self.currency_id:
                self.move_id.write({"currency_id": self.currency_id.id})

            self.move_id.invoice_line_ids.with_context({"force_delete": True}).unlink()
            self.move_id.write(
                {
                    "invoice_line_ids": val_list,
                }
            )
        else:
            for record in invoice_ids:
                for move in record.invoice_line_ids:
                    currency_id = (
                        self.currency_id
                        if self.merge_multi_currency_inv and self.currency_id
                        else move.currency_id
                    )
                    price_unit = move.currency_id._convert(move.price_unit, currency_id, move.company_id, move.invoice_date or fields.Date.today())
                    val_list.append(
                        (
                            0,
                            0,
                            {
                                "product_id": move.product_id.id,
                                "name": move.name,
                                "currency_id": currency_id.id,
                                "account_id": move.account_id.id,
                                "quantity": move.quantity,
                                "price_unit": price_unit,
                                "tax_ids": [(6, 0, move.tax_ids.ids)],
                            },
                        )
                    )

            currency_id = (
                self.currency_id
                if self.merge_multi_currency_inv and self.currency_id
                else invoice.currency_id
            )
            self.env["account.move"].create(
                {
                    "partner_id": invoice.partner_id.id,
                    "invoice_date": invoice.invoice_date,
                    "currency_id": currency_id.id,
                    "invoice_payment_term_id": invoice.invoice_payment_term_id.id,
                    "journal_id": invoice.journal_id.id,
                    "move_type": invoice.move_type,
                    "invoice_user_id": self.env.uid,
                    "invoice_line_ids": val_list,
                }
            )
        return

    def merge_invoices(self):
        context = self.env.context
        active_ids = context.get("active_ids", [])
        invoice_ids = self.env["account.move"].browse(active_ids)
        partners = invoice_ids.mapped("partner_id.name")
        if any(record.state not in ("draft") for record in invoice_ids):
            raise ValidationError(
                _("All invoice should be in draft state! If you need to proceed.")
            )

        if not all(name == partners[0] for name in partners):
            raise ValidationError(
                _("All partner must be same ! if you need to proceed. ")
            )

        if self.merge_options == "new_cancel_selected":
            self.create_invoice()
            self.invoice_cancel(invoice_ids)
        elif self.merge_options == "new_delete_all_selected":
            self.create_invoice()
            invoice_ids.unlink()
        elif self.merge_options == "merge_selected_cancel_other":
            self.create_invoice()
            if self.move_id:
                invoices = invoice_ids - self.move_id
                self.invoice_cancel(invoices)
        elif self.merge_options == "merge_selected_delete_other":
            self.create_invoice()
            if self.move_id:
                invoices = invoice_ids - self.move_id
                invoices.unlink()
