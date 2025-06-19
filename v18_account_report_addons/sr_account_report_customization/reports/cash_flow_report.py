from odoo import models, api
from datetime import date
from dateutil.relativedelta import relativedelta
import calendar
import logging

_logger = logging.getLogger(__name__)

class ReportCashFlowsIndirect(models.AbstractModel):
    _name = 'report.sr_account_report_customization.csh_flws_indt'
    _description = 'Cash Flows Indirect Method Report'

    @api.model
    def _get_report_values(self, docids=None, data=None):
        _logger.info("=== Starting _get_report_values ===")

        docs = self.env['cash.flows.indirect'].search([])
        company = self.env.company
        today = date.today()

        last_day_current_month = calendar.monthrange(today.year, today.month)[1]
        current_month_start = date(today.year, today.month, 1)
        current_month_end = date(today.year, today.month, last_day_current_month)

        prev_month_1_end = current_month_start - relativedelta(days=1)
        prev_month_1_start = date(prev_month_1_end.year, prev_month_1_end.month, 1)

        prev_month_2_end = prev_month_1_start - relativedelta(days=1)
        prev_month_2_start = date(prev_month_2_end.year, prev_month_2_end.month, 1)

        ytd_start = date(today.year, 1, 1)
        ytd_end = current_month_end

        formatted_current_month_last_date = current_month_end.strftime('%d %B %Y')

        labels = {
            'current_month': today.strftime('%b %Y').upper(),
            'prev_month_1': prev_month_1_end.strftime('%b %Y').upper(),
            'prev_month_2': prev_month_2_end.strftime('%b %Y').upper(),
            'ytd': f"YTD {today.year}"
        }

        _logger.info(f"Company: {company}")
        _logger.info(f"Labels: {labels}")

        # Map selection values to labels
        cash_flow_map = dict(
            self.env['cash.flows.indirect.line'].fields_get(['cash_flow'])['cash_flow']['selection']
        )

        # Total label mapping
        total_label_map = {
            "Operating Activities": "Adjusted profit",
            "Changes in Operating Assets And Liabilities": "Net cash provided by operating activities",
            "Investing Activities": "Net cash provided by investing activities",
            "Financing Activities": "Net cash provided by financing activities",
            "Cash and Cash Equivalents": "Net change in cash for period"
        }

        def get_balance(account, start, end):
            lines = self.env['account.move.line'].search([
                ('account_id', '=', account.id),
                ('date', '>=', start),
                ('date', '<=', end),
                ('company_id', '=', company.id),
                ('move_id.state', '=', 'posted'),
            ])
            balance = sum(line.debit - line.credit for line in lines)
            return balance

        consolidated_cash_flow_data = {}

        for doc in docs:
            for line in doc.cash_flow_ids:
                category_key = line.cash_flow
                label_text = cash_flow_map.get(category_key)

                # ✅ Skip "Cash and Cash Equivalents" here, since it's handled separately
                if label_text == "Cash and Cash Equivalents":
                    continue

                if category_key not in consolidated_cash_flow_data:
                    consolidated_cash_flow_data[category_key] = {
                        'accounts': [],
                        'totals': {
                            'prev_month_2': 0.0,
                            'prev_month_1': 0.0,
                            'current_month': 0.0,
                            'ytd': 0.0
                        },
                        'total_label': total_label_map.get(label_text, (label_text or category_key))
                    }

                entry = consolidated_cash_flow_data[category_key]
                accounts = line.operating_activities_ids

                for account in accounts:
                    prev_2 = get_balance(account, prev_month_2_start, prev_month_2_end)
                    prev_1 = get_balance(account, prev_month_1_start, prev_month_1_end)
                    curr = get_balance(account, current_month_start, current_month_end)
                    ytd = get_balance(account, ytd_start, ytd_end)

                    if any([prev_2, prev_1, curr, ytd]):
                        entry['accounts'].append({
                            'account_name': account.name,
                            'prev_month_2': prev_2,
                            'prev_month_1': prev_1,
                            'current_month': curr,
                            'ytd': ytd,
                        })

                        entry['totals']['prev_month_2'] += prev_2
                        entry['totals']['prev_month_1'] += prev_1
                        entry['totals']['current_month'] += curr
                        entry['totals']['ytd'] += ytd

        # Remove empty categories
        filtered_cash_flow_results = {
            k: v for k, v in consolidated_cash_flow_data.items() if v['accounts']
        }

        _logger.info("=== Finished _get_report_values ===")

        cash_equivalent_table = {
            'total': {'current_month': 0.0, 'prev_month_1': 0.0, 'prev_month_2': 0.0, 'ytd': 0.0},
        }
        cash_equivalent_accounts = []

        for doc in docs:
            for line in doc.cash_flow_ids:
                if cash_flow_map.get(line.cash_flow) == "Cash and Cash Equivalents":
                    for account in line.operating_activities_ids:
                        prev_2 = get_balance(account, prev_month_2_start, prev_month_2_end)
                        prev_1 = get_balance(account, prev_month_1_start, prev_month_1_end)
                        curr = get_balance(account, current_month_start, current_month_end)
                        ytd = get_balance(account, ytd_start, ytd_end)

                        # Only include if any period has non-zero value
                        if any([prev_2, prev_1, curr, ytd]):
                            # Append account line
                            cash_equivalent_accounts.append({
                                'account_name': account.name,
                                'prev_month_2': prev_2,
                                'prev_month_1': prev_1,
                                'current_month': curr,
                                'ytd': ytd,
                            })

                            # Add to totals
                            cash_equivalent_table['total']['prev_month_2'] += prev_2
                            cash_equivalent_table['total']['prev_month_1'] += prev_1
                            cash_equivalent_table['total']['current_month'] += curr
                            cash_equivalent_table['total']['ytd'] += ytd

        # Calculate net cash total (operating + investing - financing)
        net_cash_total = {
            'current_month': 0.0,
            'prev_month_1': 0.0,
            'prev_month_2': 0.0,
            'ytd': 0.0
        }

        for key, data in consolidated_cash_flow_data.items():
            label = cash_flow_map.get(key)
            if label in ["Changes in operating assets and liabilities", "Investing Activities", "Financing Activities"]:
                factor = 1.0 if label != "Financing Activities" else -1.0
                net_cash_total['current_month'] += factor * data['totals']['current_month']
                net_cash_total['prev_month_1'] += factor * data['totals']['prev_month_1']
                net_cash_total['prev_month_2'] += factor * data['totals']['prev_month_2']
                net_cash_total['ytd'] += factor * data['totals']['ytd']

        # ✅ Determine if the "Net Cash Flows" row should be shown
        show_net_cash_flows_row = any(
            data.get('total_label') in [
                "Net cash provided by operating activities",
                "Net cash provided by investing activities",
                "Net cash provided by financing activities"
            ] and data['accounts']
            for data in consolidated_cash_flow_data.values()
        )
        print("=========================",show_net_cash_flows_row)

        return {
            'docs': docs,
            'res_company': company,
            'current_month_last_date': formatted_current_month_last_date,
            'labels': labels,
            'cash_flow_map': cash_flow_map,
            'cash_flow_results': filtered_cash_flow_results,
            'net_cash_total': net_cash_total,
            'show_net_cash_flows_row': show_net_cash_flows_row,
            'cash_equivalent_table': cash_equivalent_table,  # totals
            'cash_equivalent_accounts': cash_equivalent_accounts,
        }
