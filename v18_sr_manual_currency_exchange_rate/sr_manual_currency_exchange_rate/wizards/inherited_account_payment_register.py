# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from collections import defaultdict
from odoo import models, fields, api, _


class srAccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    apply_manual_currency_exchange = fields.Boolean(string='Apply Manual Currency Exchange')
    manual_currency_exchange_rate = fields.Float(string='Manual Currency Exchange Rate',digits='Manual Currency')
    active_manual_currency_rate = fields.Boolean('active Manual Currency', default=False)
    journal_amount = fields.Float("Amount", readonly=True)

    @api.onchange('manual_currency_exchange_rate', 'amount', 'currency_id')
    def onchange_manual_currency_exchange_rate(self):
        if self.apply_manual_currency_exchange:
            self.journal_amount = self.manual_currency_exchange_rate * self.amount

    # New Code
    @api.onchange('currency_id')
    def _onchange_currency_id(self):
        if self.currency_id:
            if self.company_id.currency_id != self.currency_id:
                self.active_manual_currency_rate = True
            else:
                self.active_manual_currency_rate = False
        else:
            self.active_manual_currency_rate = False

        if not self.can_edit_wizard or not self.currency_id or not self.payment_date or not self.custom_user_amount:
            return

        if self.custom_user_amount:
            self.custom_user_amount = self.amount = self.custom_user_currency_id._convert(
                from_amount=self.custom_user_amount,
                to_currency=self.currency_id,
                date=self.payment_date,
                company=self.company_id,
            )
            
    def _convert_to_wizard_currency(self, installments):
        self.ensure_one()
        total_per_currency = defaultdict(lambda: {
            'amount_residual': 0.0,
            'amount_residual_currency': 0.0,
        })
        for installment in installments:
            line = installment['line']
            total_per_currency[line.currency_id]['amount_residual'] += installment['amount_residual']
            total_per_currency[line.currency_id]['amount_residual_currency'] += installment['amount_residual_currency']

        total_amount = 0.0
        wizard_curr = self.currency_id
        comp_curr = self.company_currency_id
        for currency, amounts in total_per_currency.items():
            amount_residual = amounts['amount_residual']
            amount_residual_currency = amounts['amount_residual_currency']
            if currency == wizard_curr:
                # Same currency
                total_amount += amount_residual_currency
            elif currency != comp_curr and wizard_curr == comp_curr:
                # Foreign currency on source line but the company currency one on the opposite line.
                if self.apply_manual_currency_exchange and self.manual_currency_exchange_rate:
                    # return self.source_currency_custom_rate(self.source_amount_currency)
                    # total_amount += currency.with_context(
                    #     cus_manual_rate=self.manual_currency_exchange_rate,
                    #     cus_active_manutal_currency=self.apply_manual_currency_exchange,
                    # )._convert(
                    #     self.source_amount_currency,
                    #     comp_curr,
                    #     self.company_id,
                    #     self.payment_date,
                    # ), False
                    converted_amount = currency.with_context(
                        cus_manual_rate=self.manual_currency_exchange_rate,
                        cus_active_manutal_currency=self.apply_manual_currency_exchange,
                    )._convert(
                        self.source_amount_currency,
                        comp_curr,
                        self.company_id,
                        self.payment_date,
                    )
                    total_amount += converted_amount
                else:
                    total_amount += currency._convert(amount_residual_currency, comp_curr, self.company_id,
                                                      self.payment_date)
            elif currency == comp_curr and wizard_curr != comp_curr:
                # Company currency on source line but a foreign currency one on the opposite line.
                if self.apply_manual_currency_exchange and self.manual_currency_exchange_rate:
                    comp_curr_converted_amount = comp_curr.with_context(
                        diff_manual_rate=self.manual_currency_exchange_rate,
                        diff_active_manutal_currency=self.apply_manual_currency_exchange,
                    )._convert(
                        amount_residual,
                        self.currency_id,
                        self.company_id,
                        self.payment_date,
                    )
                    total_amount += comp_curr_converted_amount
                else:
                    total_amount += comp_curr._convert(amount_residual, wizard_curr, self.company_id, self.payment_date)
            else:
                # Foreign currency on payment different than the one set on the journal entries.
                total_amount += comp_curr._convert(amount_residual, wizard_curr, self.company_id, self.payment_date)
        return total_amount

    # New Code
    # @api.depends('can_edit_wizard', 'source_amount', 'source_amount_currency', 'source_currency_id',
    #              'company_id', 'currency_id', 'payment_date', 'installments_mode', 'apply_manual_currency_exchange',
    #              'manual_currency_exchange_rate','active_manual_currency_rate')
    # def _compute_amount(self):
    #     return super(srAccountPaymentRegister, self)._compute_amount()

    # New code
    @api.model
    def default_get(self, fields):
        result = super(srAccountPaymentRegister, self).default_get(fields)
        # move_id = self.env['account.move'].browse(self._context.get('active_ids')).filtered(lambda move: move.is_invoice(include_receipts=True))
        move_id = self.env['account.move.line'].browse(self._context.get('active_ids')).filtered(lambda move: move.move_id.is_invoice(include_receipts=True))
        if len(move_id.move_id) !=1:
            return result
        else:
            result.update({
                'apply_manual_currency_exchange': move_id.move_id.apply_manual_currency_exchange,
                'manual_currency_exchange_rate': move_id.move_id.manual_currency_exchange_rate,
            })
            return result

    # New Code
    @api.depends('can_edit_wizard', 'amount', 'installments_mode' , 'manual_currency_exchange_rate', 'apply_manual_currency_exchange')
    def _compute_payment_difference(self):
        for wizard in self:
            if wizard.payment_date:
                total_amount_values = wizard._get_total_amounts_to_pay(wizard.batches)
                if wizard.installments_mode in ('overdue', 'next', 'before_date'):
                    wizard.payment_difference = total_amount_values['amount_for_difference'] - wizard.amount
                elif wizard.installments_mode == 'full':
                    wizard.payment_difference = total_amount_values['full_amount_for_difference'] - wizard.amount
                else:
                    if wizard.apply_manual_currency_exchange:
                        amount_payment_currency = wizard.company_id.currency_id.with_context(
                            manual_rate=wizard.manual_currency_exchange_rate,
                            active_manutal_currency = wizard.apply_manual_currency_exchange,
                        )._convert(wizard.source_amount, wizard.currency_id, wizard.company_id, wizard.payment_date)
                        wizard.payment_difference = amount_payment_currency - wizard.amount
                    else:
                        wizard.payment_difference = total_amount_values['amount_for_difference'] - wizard.amount
            else:
                wizard.payment_difference = 0.0

    def _create_payment_vals_from_wizard(self, batch_result):
        payment_vals = {
            'date': self.payment_date,
            'amount': self.amount,
            'payment_type': self.payment_type,
            'partner_type': self.partner_type,
            'memo': self.communication,
            'journal_id': self.journal_id.id,
            'company_id': self.company_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'partner_bank_id': self.partner_bank_id.id,
            'payment_method_line_id': self.payment_method_line_id.id,
            'destination_account_id': self.line_ids[0].account_id.id,
            'write_off_line_vals': [],
            'apply_manual_currency_exchange':self.apply_manual_currency_exchange,
            'manual_currency_exchange_rate':self.manual_currency_exchange_rate,
            'active_manual_currency_rate':self.active_manual_currency_rate
        }

        if self.payment_difference_handling == 'reconcile':
            if self.early_payment_discount_mode:
                epd_aml_values_list = []
                for aml in batch_result['lines']:
                    if aml.move_id._is_eligible_for_early_payment_discount(self.currency_id, self.payment_date):
                        epd_aml_values_list.append({
                            'aml': aml,
                            'amount_currency': -aml.amount_residual_currency,
                            'balance': aml.currency_id._convert(-aml.amount_residual_currency, aml.company_currency_id, date=self.payment_date),
                        })

                open_amount_currency = self.payment_difference * (-1 if self.payment_type == 'outbound' else 1)
                open_balance = self.currency_id._convert(open_amount_currency, self.company_id.currency_id, self.company_id, self.payment_date)
                early_payment_values = self.env['account.move']._get_invoice_counterpart_amls_for_early_payment_discount(epd_aml_values_list, open_balance)
                for aml_values_list in early_payment_values.values():
                    payment_vals['write_off_line_vals'] += aml_values_list

            elif not self.currency_id.is_zero(self.payment_difference):

                if self.writeoff_is_exchange_account:
                    # Force the rate when computing the 'balance' only when the payment has a foreign currency.
                    # If not, the rate is forced during the reconciliation to put the difference directly on the
                    # exchange difference.
                    if self.currency_id != self.company_currency_id:
                        payment_vals['force_balance'] = sum(batch_result['lines'].mapped('amount_residual'))
                else:
                    if self.payment_type == 'inbound':
                        # Receive money.
                        write_off_amount_currency = self.payment_difference
                    else:  # if self.payment_type == 'outbound':
                        # Send money.
                        write_off_amount_currency = -self.payment_difference

                    payment_vals['write_off_line_vals'].append({
                        'name': self.writeoff_label,
                        'account_id': self.writeoff_account_id.id,
                        'partner_id': self.partner_id.id,
                        'currency_id': self.currency_id.id,
                        'amount_currency': write_off_amount_currency,
                        'balance': self.currency_id._convert(write_off_amount_currency, self.company_id.currency_id, self.company_id, self.payment_date),
                    })
        return payment_vals

    def _create_payment_vals_from_batch(self, batch_result):
        batch_values = self._get_wizard_values_from_batch(batch_result)

        if batch_values['payment_type'] == 'inbound':
            partner_bank_id = self.journal_id.bank_account_id.id
        else:
            partner_bank_id = batch_result['payment_values']['partner_bank_id']

        payment_method_line = self.payment_method_line_id

        if batch_values['payment_type'] != payment_method_line.payment_type:
            payment_method_line = self.journal_id._get_available_payment_method_lines(batch_values['payment_type'])[:1]

        payment_vals = {
            'date': self.payment_date,
            'amount': batch_values['source_amount_currency'],
            'payment_type': batch_values['payment_type'],
            'partner_type': batch_values['partner_type'],
            'memo': self._get_communication(batch_result['lines']),
            'journal_id': self.journal_id.id,
            'company_id': self.company_id.id,
            'currency_id': batch_values['source_currency_id'],
            'partner_id': batch_values['partner_id'],
            'payment_method_line_id': payment_method_line.id,
            'destination_account_id': batch_result['lines'][0].account_id.id,
            'write_off_line_vals': [],
            'apply_manual_currency_exchange': self.apply_manual_currency_exchange,
            'manual_currency_exchange_rate': self.manual_currency_exchange_rate,
            'active_manual_currency_rate': self.active_manual_currency_rate
        }
        # In case it is false, we don't add it to the create vals so that
        # _compute_partner_bank_id is executed at payment creation
        if partner_bank_id:
            payment_vals['partner_bank_id'] = partner_bank_id

        total_amount_values = self._get_total_amounts_to_pay([batch_result])
        total_amount = total_amount_values['amount_by_default']
        currency = self.env['res.currency'].browse(batch_values['source_currency_id'])
        if total_amount_values['epd_applied']:
            payment_vals['amount'] = total_amount

            epd_aml_values_list = []
            for aml in batch_result['lines']:
                if aml.move_id._is_eligible_for_early_payment_discount(currency, self.payment_date):
                    epd_aml_values_list.append({
                        'aml': aml,
                        'amount_currency': -aml.amount_residual_currency,
                        'balance': currency._convert(-aml.amount_residual_currency, aml.company_currency_id,
                                                     self.company_id, self.payment_date),
                    })

            open_amount_currency = (batch_values['source_amount_currency'] - total_amount) * (
                -1 if batch_values['payment_type'] == 'outbound' else 1)
            open_balance = currency._convert(open_amount_currency, aml.company_currency_id, self.company_id,
                                             self.payment_date)
            early_payment_values = self.env['account.move'] \
                ._get_invoice_counterpart_amls_for_early_payment_discount(epd_aml_values_list, open_balance)
            for aml_values_list in early_payment_values.values():
                payment_vals['write_off_line_vals'] += aml_values_list

        return payment_vals

    def _init_payments(self, to_process, edit_mode=False):
        """ Create the payments.

        :param to_process:  A list of python dictionary, one for each payment to create, containing:
                            * create_vals:  The values used for the 'create' method.
                            * to_reconcile: The journal items to perform the reconciliation.
                            * batch:        A python dict containing everything you want about the source journal items
                                            to which a payment will be created (see '_compute_batches').
        :param edit_mode:   Is the wizard in edition mode.
        """

        payments = self.env['account.payment'] \
            .with_context(skip_invoice_sync=True) \
            .create([x['create_vals'] for x in to_process])

        for payment, vals in zip(payments, to_process):
            vals['payment'] = payment

            # If payments are made using a currency different than the source one, ensure the balance match exactly in
            # order to fully paid the source journal items.
            # For example, suppose a new currency B having a rate 100:1 regarding the company currency A.
            # If you try to pay 12.15A using 0.12B, the computed balance will be 12.00A for the payment instead of 12.15A.
            if edit_mode and payment.move_id:
                lines = vals['to_reconcile']

                # Batches are made using the same currency so making 'lines.currency_id' is ok.
                if payment.currency_id != lines.currency_id:
                    liquidity_lines, counterpart_lines, writeoff_lines = payment._seek_for_lines()
                    source_balance = abs(sum(lines.mapped('amount_residual')))
                    if self.apply_manual_currency_exchange:
                        payment_rate = self.manual_currency_exchange_rate
                    else:
                        if liquidity_lines[0].balance:
                            payment_rate = liquidity_lines[0].amount_currency / liquidity_lines[0].balance
                        else:
                            payment_rate = 0.0
                    source_balance_converted = abs(source_balance) * payment_rate

                    # Translate the balance into the payment currency is order to be able to compare them.
                    # In case in both have the same value (12.15 * 0.01 ~= 0.12 in our example), it means the user
                    # attempt to fully paid the source lines and then, we need to manually fix them to get a perfect
                    # match.
                    if self.apply_manual_currency_exchange:
                        payment_balance = abs(sum(counterpart_lines.mapped('balance'))) * self.manual_currency_exchange_rate
                        payment_amount_currency = abs(sum(counterpart_lines.mapped('amount_currency')))# * self.manual_currency_exchange_rate
                    else:
                        payment_balance = abs(sum(counterpart_lines.mapped('balance')))
                        payment_amount_currency = abs(sum(counterpart_lines.mapped('amount_currency')))
                    if not payment.currency_id.is_zero(source_balance_converted - payment_amount_currency):
                        continue

                    delta_balance = source_balance - payment_balance

                    # Balance are already the same.
                    if self.company_currency_id.is_zero(delta_balance):
                        continue

                    # Fix the balance but make sure to peek the liquidity and counterpart lines first.
                    debit_lines = (liquidity_lines + counterpart_lines).filtered('debit')
                    credit_lines = (liquidity_lines + counterpart_lines).filtered('credit')

                    if debit_lines and credit_lines:
                        payment.move_id.write({'line_ids': [
                            (1, debit_lines[0].id, {'debit': debit_lines[0].debit + delta_balance}),
                            (1, credit_lines[0].id, {'credit': credit_lines[0].credit + delta_balance}),
                        ]})
        return payments
