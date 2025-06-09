from calendar import monthrange
from odoo import models, api
from datetime import date
import calendar
from dateutil.relativedelta import relativedelta


class AgedPayableReport(models.AbstractModel):
    _name = 'report.sr_account_report_customization.aged_payable_report'
    _description = 'Aged Payable Report'

    @api.model
    def _get_report_values(self, docids=None, data=None):
        docs = self.env['aged.payables.summary'].search([], limit=1)
        today = date.today()
        last_day = date(today.year, today.month, monthrange(today.year, today.month)[1])

        def get_aging_buckets():
            buckets = []
            for i in range(0, 4):
                ref_date = today - relativedelta(months=i)
                start = ref_date.replace(day=1)
                end = ref_date.replace(day=calendar.monthrange(ref_date.year, ref_date.month)[1])
                label = "< 1 MONTH" if i == 0 else f"{i} MONTH"
                buckets.append((label, start, end))

            older_end = buckets[-1][1] - relativedelta(days=1)
            buckets.append(("OLDER", None, older_end))
            return buckets

        def get_account_balances(account, date_buckets):
            result = {}
            total = 0.0
            for label, start, end in date_buckets:
                domain = [
                    ('account_id', '=', account.id),
                    ('company_id', '=', self.env.company.id),
                    ('move_id.state', '=', 'posted'),
                ]
                if label == "OLDER":
                    domain.append(('date', '<=', end))
                else:
                    domain += [('date', '>=', start), ('date', '<=', end)]
                lines = self.env['account.move.line'].search(domain)
                balance = sum(line.debit - line.credit for line in lines)
                result[label] = balance
                total += balance
            result['TOTAL'] = total
            return result

        report_lines = []
        totals = {label: 0.0 for label, _, _ in get_aging_buckets()}
        totals['TOTAL'] = 0.0

        if docs and docs.aged_payable_ids:
            for acc in docs.aged_payable_ids:
                balances = get_account_balances(acc, get_aging_buckets())

                if all(value == 0.0 for key, value in balances.items()):
                    continue

                report_lines.append({
                    'account_name': acc.name,
                    **balances
                })
                for key in balances:
                    totals[key] += balances[key]

        return {
            'doc_ids': docs.ids,
            'doc_model': 'aged.payables.summary',
            'res_company': self.env.company,
            'docs': docs,
            'report_lines': report_lines,
            'totals': totals,
            'report_date': last_day.strftime('%d %B %Y'),
           }