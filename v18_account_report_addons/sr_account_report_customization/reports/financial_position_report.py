from odoo import fields, models, api, _
from datetime import date
import calendar
from dateutil.relativedelta import relativedelta
from collections import defaultdict

class FinancialPosition(models.AbstractModel):
    _name = 'report.sr_account_report_customization.fin_pos_report'
    _description = 'Report Financial Position'

    def _get_last_date_of_current_month(self):
        today = date.today()
        last_day = calendar.monthrange(today.year, today.month)[1]
        last_date = date(today.year, today.month, last_day)
        return last_date.strftime('%d %b %Y')

    def _month_range(self, dt):
        """Return first and last date of the given month."""
        start = dt.replace(day=1)
        end = dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])
        return start, end

    def format_amount(self, amount):
        if amount < 0:
            return f"({abs(amount):,.2f})"
        else:
            return f"{amount:,.2f}"

    def get_balance(self, account, start, end):
        lines = self.env['account.move.line'].search([
            ('account_id', '=', account.id),
            ('date', '>=', start),
            ('date', '<=', end),
            ('company_id', '=', self.env.company.id),
            ('move_id.state', '=', 'posted'),
        ])
        return sum(line.debit - line.credit for line in lines)

    @api.model
    def _get_report_values(self, docids=None, data=None):
        docs = self.env['financial.position'].search([])
        current_date = self._get_last_date_of_current_month()
        today = date.today()

        def get_month_end(dt):
            last_day = calendar.monthrange(dt.year, dt.month)[1]
            return date(dt.year, dt.month, last_day)

        # Calculate month-end dates
        current_month_end = get_month_end(today)
        prev_month_1_end = get_month_end(today - relativedelta(months=1))
        prev_month_2_end = get_month_end(today - relativedelta(months=2))
        last_year_end = date(today.year - 1, 12, 31)

        # YTD (optional)
        ytd_start = date(today.year, 1, 1)
        ytd_end = today

        labels = {
            'current_month': current_month_end.strftime('%d %b %Y'),
            'prev_month_1': prev_month_1_end.strftime('%d %b %Y'),
            'prev_month_2': prev_month_2_end.strftime('%d %b %Y'),
            'lytd': last_year_end.strftime('%d %b %Y'),
            # 'ytd': f"{ytd_start.strftime('%d %b')} - {ytd_end.strftime('%d %b %Y')}",
        }

        def month_label_and_range(d):
            start = d.replace(day=1)
            end = d.replace(day=calendar.monthrange(d.year, d.month)[1])
            label = d.strftime('%B %Y')
            return label, start, end

        # Label and ranges
        current_label, current_start, current_end = month_label_and_range(today)
        previous_label, previous_start, previous_end = month_label_and_range(today - relativedelta(months=1))
        previous_previous_label, previous_previous_start, previous_previous_end = month_label_and_range(
            today - relativedelta(months=2))

        grouped_results = defaultdict(list)
        grouped_totals = defaultdict(lambda: {'current': 0.0, 'previous': 0.0, 'prev_prev': 0.0})


        for doc in docs:
            for line in doc.financial_position_ids:
                asset_label = dict(line._fields['assets'].selection).get(line.assets)
                for acc in line.account_ids:
                    cur = self.get_balance(acc, current_start, current_end)
                    prev = self.get_balance(acc, previous_start, previous_end)
                    prev_prev = self.get_balance(acc, previous_previous_start, previous_previous_end)

                    if cur == 0 and prev == 0 and prev_prev == 0:
                        continue

                    grouped_results[asset_label].append({
                        'account_name': acc.name,
                        'current_month': cur,
                        'previous_month': prev,
                        'previous_previous_month': prev_prev,
                    })

                    grouped_totals[asset_label]['current'] += cur
                    grouped_totals[asset_label]['previous'] += prev
                    grouped_totals[asset_label]['prev_prev'] += prev_prev

        total_assets = {
            'current': 0.0,
            'previous': 0.0,
            'prev_prev': 0.0
        }
        for totals in grouped_totals.values():
            total_assets['current'] += totals['current']
            total_assets['previous'] += totals['previous']
            total_assets['prev_prev'] += totals['prev_prev']

        equity_grouped_results = defaultdict(list)
        equity_grouped_totals = defaultdict(lambda: {'current': 0.0, 'previous': 0.0, 'prev_prev': 0.0})

        # Variables to hold total Non-Current and Current Liabilities
        total_non_current = {'current': 0.0, 'previous': 0.0, 'prev_prev': 0.0}
        total_current = {'current': 0.0, 'previous': 0.0, 'prev_prev': 0.0}

        for doc in docs:
            for line in doc.equity_liabilities_ids:
                equity_label = dict(line._fields['equity_liabilities'].selection).get(line.equity_liabilities)
                for acc in line.account_ids:
                    cur = self.get_balance(acc, current_start, current_end)
                    prev = self.get_balance(acc, previous_start, previous_end)
                    prev_prev = self.get_balance(acc, previous_previous_start, previous_previous_end)

                    if cur == 0 and prev == 0 and prev_prev == 0:
                        continue

                    equity_grouped_results[equity_label].append({
                        'account_name': acc.name,
                        'current_month': cur,
                        'previous_month': prev,
                        'previous_previous_month': prev_prev,
                    })

                    equity_grouped_totals[equity_label]['current'] += cur
                    equity_grouped_totals[equity_label]['previous'] += prev
                    equity_grouped_totals[equity_label]['prev_prev'] += prev_prev


                    if line.equity_liabilities == 'non_current_liabilities':
                        total_non_current['current'] += cur
                        total_non_current['previous'] += prev
                        total_non_current['prev_prev'] += prev_prev
                    elif line.equity_liabilities == 'current_liabilities':
                        total_current['current'] += cur
                        total_current['previous'] += prev
                        total_current['prev_prev'] += prev_prev

        total_liabilities = {
            'current': total_non_current['current'] + total_current['current'],
            'previous': total_non_current['previous'] + total_current['previous'],
            'prev_prev': total_non_current['prev_prev'] + total_current['prev_prev'],
        }

        total_equity_liabilities = {
            'current': 0.0,
            'previous': 0.0,
            'prev_prev': 0.0
        }

        for totals in equity_grouped_totals.values():
            total_equity_liabilities['current'] += totals['current']
            total_equity_liabilities['previous'] += totals['previous']
            total_equity_liabilities['prev_prev'] += totals['prev_prev']


        return {
            'doc_model': 'financial.position',
            'docs': docs,
            'date': current_date,
            'res_company': self.env.company,

            'labels': labels,

            'current_month_label': current_label,
            'previous_month_label': previous_label,
            'previous_previous_month_label': previous_previous_label,

            'format_amount': self.format_amount,

            'grouped_results': dict(grouped_results),
            'grouped_totals': dict(grouped_totals),

            'total_assets': total_assets,

            'equity_grouped_results': dict(equity_grouped_results),
            'equity_grouped_totals': dict(equity_grouped_totals),

            'combined_liabilities_total': total_liabilities,

            'total_equity_liabilities': total_equity_liabilities,

        }
