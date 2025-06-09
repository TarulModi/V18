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
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    internal_payment_transfer_type = fields.Selection([('account_to_account', 'Account To Account'), ('journal_to_journal', 'Journal To Journal'), ('journal_to_account', 'Journal To Account'), ('account_to_journal', 'Account To Journal')], string=' Internal Payment Transfer Type', default='account_to_account')
    destination_journal_id = fields.Many2one('account.journal', string="Destination Journal")
    source_account_id = fields.Many2one('account.account', string="Source Account")
    custom_destination_account_id = fields.Many2one('account.account', string="Destination Account")

    @api.depends('partner_id', 'journal_id', 'destination_journal_id')
    def _compute_is_internal_transfer(self):
        for payment in self:
            payment.is_internal_transfer = payment.partner_id and payment.partner_id == payment.journal_id.company_id.partner_id

    def _prepare_move_line_default_vals(self, write_off_line_vals=None, force_balance=None):
        ''' Prepare the dictionary to create the default account.move.lines for the current payment.
        :param write_off_line_vals: Optional list of dictionaries to create a write-off account.move.line easily containing:
            * amount:       The amount to be added to the counterpart amount.
            * name:         The label to set on the line.
            * account_id:   The account on which create the write-off.
        :param force_balance: Optional balance.
        :return: A list of python dictionary to be passed to the account.move.line's 'create' method.
        '''
        self.ensure_one()
        write_off_line_vals = write_off_line_vals or {}

        if not self.outstanding_account_id:
            raise UserError(_(
                "You can't create a new payment without an outstanding payments/receipts account set either on the company or the %s payment method in the %s journal.",
                self.payment_method_line_id.name, self.journal_id.display_name))


        # Compute amounts.
        write_off_amount_currency = write_off_line_vals.get('amount', 0.0)

        if self.payment_type == 'inbound':
            # Receive money.
            liquidity_amount_currency = self.amount
        elif self.payment_type == 'outbound':
            # Send money.
            liquidity_amount_currency = -self.amount
            write_off_amount_currency *= -1
        else:
            liquidity_amount_currency = write_off_amount_currency = 0.0

        write_off_balance = self.currency_id._convert(
            write_off_amount_currency,
            self.company_id.currency_id,
            self.company_id,
            self.date,
        )

        if not write_off_line_vals and force_balance is not None:
            sign = 1 if liquidity_amount_currency > 0 else -1
            liquidity_balance = sign * abs(force_balance)
        else:
            liquidity_balance = self.currency_id._convert(
                liquidity_amount_currency,
                self.company_id.currency_id,
                self.company_id,
                self.date,
            )
        counterpart_amount_currency = -liquidity_amount_currency - write_off_amount_currency
        counterpart_balance = -liquidity_balance - write_off_balance
        currency_id = self.currency_id.id

        if self.is_internal_transfer:
            if self.payment_type == 'inbound':
                if self.internal_payment_transfer_type == 'account_to_account' or self.internal_payment_transfer_type == 'journal_to_account':
                    liquidity_line_name = _('Transfer to %s', self.custom_destination_account_id.name)
                elif self.internal_payment_transfer_type == 'journal_to_journal' or self.internal_payment_transfer_type == 'account_to_journal':
                    liquidity_line_name = _('Transfer to %s', self.destination_journal_id.name)
                else:
                    liquidity_line_name = _('Transfer to %s', self.journal_id.name)
            else:  # payment.payment_type == 'outbound':
                if self.internal_payment_transfer_type == 'account_to_account' or self.internal_payment_transfer_type == 'account_to_journal':
                    liquidity_line_name = _('Transfer from %s', self.source_account_id.name)
                else:
                    liquidity_line_name = _('Transfer from %s', self.journal_id.name)
        else:
            liquidity_line_name = self.payment_reference

        if self.is_internal_transfer:
            if self.payment_type == 'inbound':
                if self.internal_payment_transfer_type == 'account_to_account':
                    liquidity_line_account_id = self.source_account_id.id
                    payment_line_account_id = self.custom_destination_account_id.id
                elif self.internal_payment_transfer_type == 'journal_to_account':
                    liquidity_line_account_id = self.journal_id.default_account_id.id
                    payment_line_account_id = self.custom_destination_account_id.id
                elif self.internal_payment_transfer_type == 'journal_to_journal':
                    liquidity_line_account_id = self.journal_id.default_account_id.id
                    payment_line_account_id = self.destination_journal_id.default_account_id.id
                elif self.internal_payment_transfer_type == 'account_to_journal':
                    liquidity_line_account_id = self.source_account_id.id
                    payment_line_account_id = self.destination_journal_id.default_account_id.id
                else:
                    raise UserError(_("Please select payment transfer type."))
            else:
                if self.internal_payment_transfer_type == 'account_to_account':
                    liquidity_line_account_id = self.custom_destination_account_id.id
                    payment_line_account_id = self.source_account_id.id
                elif self.internal_payment_transfer_type == 'journal_to_account':
                    liquidity_line_account_id = self.custom_destination_account_id.id
                    payment_line_account_id = self.journal_id.default_account_id.id
                elif self.internal_payment_transfer_type == 'journal_to_journal':
                    liquidity_line_account_id = self.destination_journal_id.default_account_id.id
                    payment_line_account_id = self.journal_id.default_account_id.id
                elif self.internal_payment_transfer_type == 'account_to_journal':
                    liquidity_line_account_id = self.destination_journal_id.default_account_id.id
                    payment_line_account_id = self.source_account_id.id
                else:
                    raise UserError(_("Please select payment transfer type."))
        else:
            liquidity_line_account_id = self.outstanding_account_id.id
            payment_line_account_id = self.destination_account_id.id


        # Compute a default label to set on the journal items.
        liquidity_line_name = ''.join(x[1] for x in self._get_liquidity_aml_display_name_list())
        counterpart_line_name = ''.join(x[1] for x in self._get_counterpart_aml_display_name_list())


        line_vals_list = [
            # Liquidity line.
            {
                'name': liquidity_line_name,
                'date_maturity': self.date,
                'amount_currency': liquidity_amount_currency,
                'currency_id': currency_id,
                'debit': liquidity_balance if liquidity_balance > 0.0 else 0.0,
                'credit':-liquidity_balance if liquidity_balance < 0.0 else 0.0,
                'partner_id': self.partner_id.id,
                'account_id': liquidity_line_account_id,
            },
            # Receivable / Payable.
            {
                'name': counterpart_line_name,
                'date_maturity': self.date,
                'amount_currency': counterpart_amount_currency,
                'currency_id': currency_id,
                'debit': counterpart_balance if counterpart_balance > 0.0 else 0.0,
                'credit':-counterpart_balance if counterpart_balance < 0.0 else 0.0,
                'partner_id': self.partner_id.id,
                'account_id': payment_line_account_id,
            },
        ]
        print ("==========line_vals_list", line_vals_list)
        print ("=======not self.currency_id.is_zero(write_off_amount_currency)", not self.currency_id.is_zero(write_off_amount_currency))
        if not self.currency_id.is_zero(write_off_amount_currency):
            # Write-off line.
            line_vals_list.append({
                'name': write_off_line_vals.get('name') or default_line_name,
                'amount_currency': write_off_amount_currency,
                'currency_id': currency_id,
                'debit': write_off_balance if write_off_balance > 0.0 else 0.0,
                'credit':-write_off_balance if write_off_balance < 0.0 else 0.0,
                'partner_id': self.partner_id.id,
                'account_id': write_off_line_vals.get('account_id'),
            })
        return line_vals_list

    def _create_paired_internal_transfer_payment(self):
        pass

    def _synchronize_from_moves(self, changed_fields):
        ''' Update the account.payment regarding its related account.move.
        Also, check both models are still consistent.
        :param changed_fields: A set containing all modified fields on account.move.
        '''
        if self._context.get('skip_account_move_synchronization'):
            return

        for pay in self.with_context(skip_account_move_synchronization=True):

            # After the migration to 14.0, the journal entry could be shared between the account.payment and the
            # account.bank.statement.line. In that case, the synchronization will only be made with the statement line.
            if pay.move_id.statement_line_id:
                continue

            move = pay.move_id
            move_vals_to_write = {}
            payment_vals_to_write = {}

            if 'journal_id' in changed_fields:
                if pay.journal_id.type not in ('bank', 'cash'):
                    raise UserError(_("A payment must always belongs to a bank or cash journal."))

            if 'line_ids' in changed_fields:
                all_lines = move.line_ids
                liquidity_lines, counterpart_lines, writeoff_lines = pay._seek_for_lines()

                if len(liquidity_lines) != 1:
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, the journal items must "
                        "include one and only one outstanding payments/receipts account.",
                        move.display_name,
                    ))

                if len(counterpart_lines) != 1:
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, the journal items must "
                        "include one and only one receivable/payable account (with an exception of "
                        "internal transfers).",
                        move.display_name,
                    ))

                if writeoff_lines and len(writeoff_lines.account_id) != 1:
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, "
                        "all optional journal items must share the same account.",
                        move.display_name,
                    ))

                if any(line.currency_id != all_lines[0].currency_id for line in all_lines):
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, the journal items must "
                        "share the same currency.",
                        move.display_name,
                    ))

                if any(line.partner_id != all_lines[0].partner_id for line in all_lines):
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, the journal items must "
                        "share the same partner.",
                        move.display_name,
                    ))

                if counterpart_lines.account_id.account_type == 'asset_receivable':
                    partner_type = 'customer'
                else:
                    partner_type = 'supplier'

                liquidity_amount = liquidity_lines.amount_currency

                move_vals_to_write.update({
                    'currency_id': liquidity_lines.currency_id.id,
                    'partner_id': liquidity_lines.partner_id.id,
                })
                payment_vals_to_write.update({
                    'amount': abs(liquidity_amount),
                    'partner_type': partner_type,
                    'currency_id': liquidity_lines.currency_id.id,
                    'destination_account_id': counterpart_lines.account_id.id,
                    'partner_id': liquidity_lines.partner_id.id,
                })
                if not pay.is_internal_transfer and not pay.internal_payment_transfer_type:
                    if liquidity_amount > 0.0:
                        payment_vals_to_write.update({'payment_type': 'inbound'})
                    elif liquidity_amount < 0.0:
                        payment_vals_to_write.update({'payment_type': 'outbound'})

            move.write(move._cleanup_write_orm_values(move, move_vals_to_write))
            pay.write(move._cleanup_write_orm_values(pay, payment_vals_to_write))