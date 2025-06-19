from odoo import fields,models,api,_
from datetime import date
import calendar
from dateutil.relativedelta import relativedelta
from collections import defaultdict

class ProfitLossStatement(models.AbstractModel):
    _name = 'report.sr_account_report_customization.profit_loss_report'
    _description = 'Profit Loss Statement Report View'

    @api.model
    def _get_report_values(self, docids=None, data=None):
        docs = self.env['profit.loss.statement'].search([])
        today = date.today()

        def month_range(dt):
            start = dt.replace(day=1)
            end = dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])
            return start, end

        current_month = today
        prev_month_1 = today - relativedelta(months=1)
        prev_month_2 = today - relativedelta(months=2)

        prev_month_2_start, prev_month_2_end = month_range(prev_month_2)
        prev_month_1_start, prev_month_1_end = month_range(prev_month_1)
        current_month_start, current_month_end = month_range(current_month)

        ytd_start = date(today.year, 1, 1)
        ytd_end = today

        current_month_last_date = current_month_end.strftime('%d %B %Y')
        labels = {
            'prev_month_2': prev_month_2.strftime('%b %Y'),
            'prev_month_1': prev_month_1.strftime('%b %Y'),
            'current_month': current_month.strftime('%b %Y'),
            'ytd': f"YTD {today.year}",
        }

        def get_balance(account, start, end):
            lines = self.env['account.move.line'].search([
                ('account_id', '=', account.id),
                ('date', '>=', start),
                ('date', '<=', end),
                ('company_id', '=', self.env.company.id),
                ('move_id.state', '=', 'posted'),
            ])
            return sum(line.debit - line.credit for line in lines)

        def format_currency(value):
            if value is None:
                return '-'
            formatted = '{:,.2f}'.format(abs(value))
            return f'({formatted})' if value < 0 else formatted

        # Changed: use dictionary instead of list
        category_map = {}
        total_operating = {'prev_month_2': 0, 'prev_month_1': 0, 'current_month': 0, 'ytd': 0}

        for doc in docs:
            for line in doc.profit_loss_statement_ids:
                accounts = line.account_ids
                if not accounts:
                    continue

                category_name = dict(
                    self.env['profit.loss.statement.line'].fields_get(allfields=['operating_expenses'])[
                        'operating_expenses']['selection']
                ).get(line.operating_expenses, "Uncategorized")

                # Initialize or get existing category
                if category_name not in category_map:
                    category_map[category_name] = {
                        'accounts': [],
                        'totals': {'prev_month_2': 0, 'prev_month_1': 0, 'current_month': 0, 'ytd': 0}
                    }

                for account in accounts:
                    prev_2 = get_balance(account, prev_month_2_start, prev_month_2_end)
                    prev_1 = get_balance(account, prev_month_1_start, prev_month_1_end)
                    curr = get_balance(account, current_month_start, current_month_end)
                    ytd = get_balance(account, ytd_start, ytd_end)

                    account_data = {
                        'account_name': account.name,
                        'prev_month_2': prev_2,
                        'prev_month_1': prev_1,
                        'current_month': curr,
                        'ytd': ytd,
                    }
                    category_map[category_name]['accounts'].append(account_data)

                    category_map[category_name]['totals']['prev_month_2'] += prev_2
                    category_map[category_name]['totals']['prev_month_1'] += prev_1
                    category_map[category_name]['totals']['current_month'] += curr
                    category_map[category_name]['totals']['ytd'] += ytd

                    total_operating['prev_month_2'] += prev_2
                    total_operating['prev_month_1'] += prev_1
                    total_operating['current_month'] += curr
                    total_operating['ytd'] += ytd

        # Final result list after merging categories
        results = [
            {
                'category': category,
                'accounts': data['accounts'],
                'totals': data['totals']
            }
            for category, data in category_map.items()
        ]

        # Non-operating expenses (unchanged)
        non_operating_expense_results = []
        total_non_op = {'prev_month_2': 0, 'prev_month_1': 0, 'current_month': 0, 'ytd': 0}

        for doc in docs:
            for account in doc.non_operating_expenses:
                prev_2 = get_balance(account, prev_month_2_start, prev_month_2_end)
                prev_1 = get_balance(account, prev_month_1_start, prev_month_1_end)
                curr = get_balance(account, current_month_start, current_month_end)
                ytd = get_balance(account, ytd_start, ytd_end)

                non_operating_expense_results.append({
                    'account_name': account.name,
                    'prev_month_2': prev_2,
                    'prev_month_1': prev_1,
                    'current_month': curr,
                    'ytd': ytd,
                })

                total_non_op['prev_month_2'] += prev_2
                total_non_op['prev_month_1'] += prev_1
                total_non_op['current_month'] += curr
                total_non_op['ytd'] += ytd

        # Static revenue placeholder
        revenue_totals = {
            'prev_month_2': 0.0,
            'prev_month_1': 0.0,
            'current_month': 0.0,
            'ytd': 0.0,
        }

        operating_profit_loss = {
            k: revenue_totals[k] + total_operating[k]
            for k in revenue_totals
        }

        total_profit_loss = {
            k: revenue_totals[k] - total_operating[k]
            for k in revenue_totals
        }

        operating_margin = {
            k: (operating_profit_loss[k] / revenue_totals[k] * 100) if revenue_totals[k] else 0.0
            for k in revenue_totals
        }

        net_profit_loss = {
            k: revenue_totals[k] - total_operating[k] - total_non_op[k]
            for k in revenue_totals
        }

        net_margin = {
            k: (net_profit_loss[k] / revenue_totals[k] * 100) if revenue_totals[k] else 0.0
            for k in revenue_totals
        }

        return {
            'doc_ids': docs.ids,
            'doc_model': 'profit.loss.statement',
            'docs': docs,
            'res_company': self.env.company,
            'current_month_last_date': current_month_last_date,
            'labels': labels,
            'results': results,
            'non_operating_expenses': non_operating_expense_results,
            'non_operating_totals': total_non_op,
            'operating_profit_loss': operating_profit_loss,
            'total_profit_loss': total_profit_loss,
            'operating_margin': operating_margin,
            'net_profit_loss': net_profit_loss,
            'net_margin': net_margin,
            'format_currency': format_currency,
        }
