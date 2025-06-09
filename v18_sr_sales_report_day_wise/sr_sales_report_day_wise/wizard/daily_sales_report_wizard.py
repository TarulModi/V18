# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

import logging
from datetime import datetime, date, timedelta
from odoo import fields, models, api
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class DailySalesReportWizard(models.TransientModel):
    _name = "daily.sales.report.wizard"
    _description = "Daily Sales Report Wizard"

    from_date = fields.Date(string="Start Date", default=lambda self: date.today() - timedelta(days=7))
    to_date = fields.Date(string="End Date")
    current_session = fields.Char(readonly=True, default="0")
    session_date = fields.Date(readonly=True, default=lambda self: date.today())

    product_id = fields.Integer(string="ID", readonly=True)
    product_name = fields.Char(string='Name', readonly=True)
    sunday = fields.Integer(string="Sunday", readonly=True)
    monday = fields.Integer(string="Monday", readonly=True)
    tuesday = fields.Integer(string="Tuesday", readonly=True)
    wednesday = fields.Integer(string="Wednesday", readonly=True)
    thursday = fields.Integer(string="Thursday", readonly=True)
    friday = fields.Integer(string="Friday", readonly=True)
    saturday = fields.Integer(string="Saturday", readonly=True)
    total = fields.Integer(string="Total", readonly=True)

    @api.onchange('from_date')
    def onchange_from_date(self):
        if self.from_date and (date.today() - self.from_date).days > 180:
            raise ValidationError("Only last 180 days data can be checked. %s is over 180 days" % self.from_date)

    @api.onchange('to_date')
    def onchange_to_date(self):
        if self.to_date and self.to_date > date.today():
            raise ValidationError("Future date can't be selected")

    @api.onchange('from_date', 'to_date')
    def onchange_from_date_to_date(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError("Please select dates correctly!")
        if not self.from_date:
            self.from_date = date.today() - timedelta(days=180)

    def get_daily_sales_report_wizard(self):
        if not self.from_date and not self.to_date:
            raise ValidationError("Dates required")

        from_date = self.from_date if self.from_date else date.today()
        to_date = self.to_date if self.to_date else date.today()

        request.session['from_date'] = from_date.isoformat()
        request.session['to_date'] = to_date.isoformat()
        request.session['print_report'] = False

    def _get_data(self):
        _logger.info('Generating data from %s to %s', self.from_date, self.to_date)
        sale_order_line_data = self.env['sale.order.line'].search([
            ('order_id.state', '!=', 'cancel')
        ])

        from_date = self.from_date
        to_date = self.to_date

        if from_date and to_date:
            order_list = [x for x in sale_order_line_data if from_date <= x.order_id.date_order.date() <= to_date]
        elif not from_date and to_date:
            order_list = [x for x in sale_order_line_data if x.order_id.date_order.date() <= to_date]
        elif from_date and not to_date:
            order_list = [x for x in sale_order_line_data if x.order_id.date_order.date() >= from_date]
        else:
            order_list = list(sale_order_line_data)

        return self._get_daywise_report_data(order_list)

    def _get_daywise_report_data(self, order):
        result = []
        product_dict = {}
        total = {i: 0 for i in range(7)}

        for rec in order:
            weekday = rec.order_id.date_order.weekday()
            days = {i: 0 for i in range(7)}
            days[weekday] = rec.product_uom_qty
            total[weekday] += rec.product_uom_qty

            product_id = rec.product_id
            p_name = rec.name if not request.session.get('print_report') else rec.name[:90]

            if product_id not in product_dict:
                product_dict[product_id] = {
                    'product_id': product_id.id,
                    'product_name': p_name,
                    'sunday': int(days[6]),
                    'monday': int(days[0]),
                    'tuesday': int(days[1]),
                    'wednesday': int(days[2]),
                    'thursday': int(days[3]),
                    'friday': int(days[4]),
                    'saturday': int(days[5]),
                    'total': rec.product_uom_qty,
                }
            else:
                day_str = rec.order_id.date_order.strftime('%A').lower()
                product_dict[product_id][day_str] += days[weekday]
                product_dict[product_id]['total'] += rec.product_uom_qty

        if request.session.get('print_report') and product_dict:
            product_dict['total'] = {
                'product_id': 0,
                'product_name': "",
                'sunday': int(total[6]),
                'monday': int(total[0]),
                'tuesday': int(total[1]),
                'wednesday': int(total[2]),
                'thursday': int(total[3]),
                'friday': int(total[4]),
                'saturday': int(total[5]),
                'total': sum(total.values()),
            }

        request.session['print_report'] = False
        return list(product_dict.values())

    def get_daily_sales_report_print(self):
        request.session['print_report'] = True
        request.session['from_date'] = self.from_date.isoformat() if self.from_date else date.today().isoformat()
        request.session['to_date'] = self.to_date.isoformat() if self.to_date else date.today().isoformat()

        record_ids = self._get_data()

        datas = {
            'ids': self,
            'model': 'daily.sales.report.wizard',
            'form': record_ids,
            'start_date': request.session['from_date'],
            'end_date': request.session['to_date'],
        }

        return self.env.ref('sr_sales_report_day_wise.action_report_daywise_saleorder').report_action([], data=datas)
