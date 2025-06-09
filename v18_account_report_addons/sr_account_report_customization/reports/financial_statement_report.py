from odoo import models, api
from datetime import date
import calendar
from dateutil.relativedelta import relativedelta

class ReportFinancialStatementNotes(models.AbstractModel):
    _name = 'report.sr_account_report_customization.finc_stm_notes'
    _description = 'Financial Statement Notes Report'

    @api.model
    def _get_report_values(self, docids=None, data=None):
        # Search for the financial statement notes document.
        # Assuming there's only one relevant record to fetch.
        docs = self.env['financial.statement.notes'].search([], limit=1)
        today = date.today()

        # Helper function to get month label and date range (start/end)
        def month_label_and_range(d):
            # Get the first day of the month
            start = d.replace(day=1)
            # Get the last day of the month using calendar.monthrange
            end = d.replace(day=calendar.monthrange(d.year, d.month)[1])
            # Format the month and year for the label
            label = d.strftime('%B %Y')
            return label, start, end

        # Calculate date ranges and labels for current, previous, and previous-previous months
        current_label, current_start, current_end = month_label_and_range(today)
        previous_label, previous_start, previous_end = month_label_and_range(today - relativedelta(months=1))
        previous_previous_label, previous_previous_start, previous_previous_end = month_label_and_range(today - relativedelta(months=2))

        # Helper function to get the balance for a given account within a date range
        def get_balance(account, start, end):
            # Search for account move lines that match the criteria
            lines = self.env['account.move.line'].search([
                ('account_id', '=', account.id),
                ('date', '>=', start),
                ('date', '<=', end),
                ('company_id', '=', self.env.company.id), # Filter by current company
                ('move_id.state', '=', 'posted'), # Only consider posted moves
            ])
            # Sum the debit minus credit for all found lines to get the balance
            return sum(line.debit - line.credit for line in lines)

        # Initialize lists to store results for different sections
        results, wip_results, cash_results = [], [], []
        related_results, emp_results = [], []
        payment_receivables_results = [] # This will hold the consolidated payment receivables

        # Initialize total variables for each section (already floats by initializing with 0.0)
        total_current = total_previous = total_previous_previous = 0.0 # PPE totals
        wip_total_current = wip_total_previous = wip_total_previous_previous = 0.0 # WIP totals
        cash_total_current = cash_total_previous = cash_total_previous_previous = 0.0 # Cash totals
        related_total_current = related_total_previous = related_total_previous_previous = 0.0 # Related Party totals
        emp_total_current = emp_total_previous = emp_total_previous_previous = 0.0 # Employee Provision totals
        # Grand totals for consolidated payment receivables
        payment_receivables_grand_total_current = 0.0
        payment_receivables_grand_total_previous = 0.0
        payment_receivables_grand_total_previous_previous = 0.0

        # --- Property, Plant and Equipment (PPE) ---
        if docs and docs.property_plant_equipment_ids:
            for acc in docs.property_plant_equipment_ids:
                cur = get_balance(acc, current_start, current_end)
                prev = get_balance(acc, previous_start, previous_end)
                prev_prev = get_balance(acc, previous_previous_start, previous_previous_end)
                # Append only if at least one balance is non-zero
                if cur != 0 or prev != 0 or prev_prev != 0:
                    results.append({
                        'account_name': acc.name,
                        'current_month': cur,
                        'previous_month': prev,
                        'previous_previous_month': prev_prev
                    })
                    total_current += cur
                    total_previous += prev
                    total_previous_previous += prev_prev

        # --- Work In Progress (WIP) ---
        if docs and docs.wip_ids:
            for acc in docs.wip_ids:
                cur = get_balance(acc, current_start, current_end)
                prev = get_balance(acc, previous_start, previous_end)
                prev_prev = get_balance(acc, previous_previous_start, previous_previous_end)
                # Append only if at least one balance is non-zero
                if cur != 0 or prev != 0 or prev_prev != 0:
                    wip_results.append({
                        'account_name': acc.name,
                        'current_month': cur,
                        'previous_month': prev,
                        'previous_previous_month': prev_prev
                    })
                    wip_total_current += cur
                    wip_total_previous += prev
                    wip_total_previous_previous += prev_prev

        # --- Cash and Cash Equivalents ---
        if docs and docs.cash_equivalents_ids:
            for acc in docs.cash_equivalents_ids:
                cur = get_balance(acc, current_start, current_end)
                prev = get_balance(acc, previous_start, previous_end)
                prev_prev = get_balance(acc, previous_previous_start, previous_previous_end)
                # Append only if at least one balance is non-zero
                if cur != 0 or prev != 0 or prev_prev != 0:
                    cash_results.append({
                        'account_name': acc.name,
                        'current_month': cur,
                        'previous_month': prev,
                        'previous_previous_month': prev_prev
                    })
                    cash_total_current += cur
                    cash_total_previous += prev
                    cash_total_previous_previous += prev_prev

        # --- Related Party Transactions ---
        if docs and docs.related_party_ids:
            for acc in docs.related_party_ids:
                cur = get_balance(acc, current_start, current_end)
                prev = get_balance(acc, previous_start, previous_end)
                prev_prev = get_balance(acc, previous_previous_start, previous_previous_end)
                # Append only if at least one balance is non-zero
                if cur != 0 or prev != 0 or prev_prev != 0:
                    related_results.append({
                        'account_name': acc.name,
                        'current_month': cur,
                        'previous_month': prev,
                        'previous_previous_month': prev_prev
                    })
                    related_total_current += cur
                    related_total_previous += prev
                    related_total_previous_previous += prev_prev

        # --- Employee Provision ---
        if docs and docs.employee_provision_ids:
            for acc in docs.employee_provision_ids:
                cur = get_balance(acc, current_start, current_end)
                prev = get_balance(acc, previous_start, previous_end)
                prev_prev = get_balance(acc, previous_previous_start, previous_previous_end)
                # Append only if at least one balance is non-zero
                if cur != 0 or prev != 0 or prev_prev != 0:
                    emp_results.append({
                        'account_name': acc.name,
                        'current_month': cur,
                        'previous_month': prev,
                        'previous_previous_month': prev_prev
                    })
                    emp_total_current += cur
                    emp_total_previous += prev
                    emp_total_previous_previous += prev_prev

        # --- Payment and Other Receivables (Group + Detailed) ---
        if docs and docs.financial_line_ids:
            # Create a map from selection value (internal code) to its human-readable label
            payment_other_receivables_selection_map = {
                value: label
                for value, label in self.env['financial.statement.notes.line']._fields['payment_other_receivables'].selection
            }

            # Use a temporary dictionary to consolidate results by category label.
            # This dictionary will store aggregated data for each unique 'payment_other_receivables' type.
            consolidated_receivables_data = {}

            for financial_line in docs.financial_line_ids:
                # Get the selection value and its corresponding label for the current financial line
                current_line_selection_value = financial_line.payment_other_receivables
                current_line_label = payment_other_receivables_selection_map.get(
                    current_line_selection_value,
                    'Unknown Category' # Fallback for cases where the selection value is not found
                )

                # If this label is encountered for the first time, initialize its entry in the consolidated data
                if current_line_label not in consolidated_receivables_data:
                    consolidated_receivables_data[current_line_label] = {
                        'label': current_line_label,
                        'lines': [], # List to hold individual account details for this consolidated category
                        'total_current': 0.0,
                        'total_previous': 0.0,
                        'total_previous_previous': 0.0,
                    }

                # Get the consolidated entry for the current label to add details and totals
                consolidated_entry = consolidated_receivables_data[current_line_label]

                # Iterate through accounts linked to the current financial line
                for acc in financial_line.account_ids:
                    # Get balances for the current account across the three periods
                    cur = get_balance(acc, current_start, current_end)
                    prev = get_balance(acc, previous_start, previous_end)
                    prev_prev = get_balance(acc, previous_previous_start, previous_previous_end)

                    # Append the account's details to the 'lines' list of the consolidated entry
                    # ONLY if at least one balance is non-zero
                    if cur != 0 or prev != 0 or prev_prev != 0:
                        consolidated_entry['lines'].append({
                            'name': acc.name,
                            'current': cur,
                            'previous': prev,
                            'previous_previous': prev_prev,
                        })

                        # Add the account's balances to the running totals of the consolidated entry
                        consolidated_entry['total_current'] += cur
                        consolidated_entry['total_previous'] += prev
                        consolidated_entry['total_previous_previous'] += prev_prev

            # After processing all financial lines, convert the dictionary values
            # into a list. This ensures that 'payment_receivables_results' contains
            # one entry for each unique payment/receivable category, with all
            # related financial lines consolidated.
            # Filter out categories that end up with no lines (i.e., all accounts were zero)
            payment_receivables_results = [
                entry for entry in consolidated_receivables_data.values() if entry['lines']
            ]

            # Recalculate the overall grand totals for payment receivables
            # by summing the 'total_current', 'total_previous', and 'total_previous_previous'
            # from the now consolidated results.
            payment_receivables_grand_total_current = sum(
                item['total_current'] for item in payment_receivables_results
            )
            payment_receivables_grand_total_previous = sum(
                item['total_previous'] for item in payment_receivables_results
            )
            payment_receivables_grand_total_previous_previous = sum(
                item['total_previous_previous'] for item in payment_receivables_results
            )

        # Return the dictionary of values to be used in the report template
        return {
            'doc_ids': docs.ids,
            'doc_model': 'financial.statement.notes',
            'docs': docs,
            'res_company': self.env.company,
            'current_month_last_date': current_end.strftime('%d %b %Y'),
            'current_month_label': current_label,
            'previous_month_label': previous_label,
            'previous_previous_month_label': previous_previous_label,

            # PPE Results
            'results': results,
            'total_current_ppe': total_current,
            'total_previous_ppe': total_previous,
            'total_previous_previous_ppe': total_previous_previous,

            # WIP Results
            'wip_results': wip_results,
            'wip_total_current': wip_total_current,
            'wip_total_previous': wip_total_previous,
            'wip_total_previous_previous': wip_total_previous_previous,

            # Cash Results
            'cash_results': cash_results,
            'cash_total_current': cash_total_current,
            'cash_total_previous': cash_total_previous,
            'cash_total_previous_previous': cash_total_previous_previous,

            # Related Party Results
            'related_results': related_results,
            'related_total_current': related_total_current,
            'related_total_previous': related_total_previous,
            'related_total_previous_previous': related_total_previous_previous,

            # Employee Provision Results
            'emp_results': emp_results,
            'emp_total_current': emp_total_current,
            'emp_total_previous': emp_total_previous,
            'emp_total_previous_previous': emp_total_previous_previous,

            # Consolidated Payment and Other Receivables Results
            'payment_receivables_results': payment_receivables_results,
            'payment_receivables_grand_total_current': payment_receivables_grand_total_current,
            'payment_receivables_grand_total_previous': payment_receivables_grand_total_previous,
            'payment_receivables_grand_total_previous_previous': payment_receivables_grand_total_previous_previous,
        }