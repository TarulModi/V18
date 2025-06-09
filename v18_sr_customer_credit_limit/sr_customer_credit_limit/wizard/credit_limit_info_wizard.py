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
from odoo import SUPERUSER_ID


class CreditLimitInfoWizard(models.TransientModel):
    _name = "credit.limit.wizard"
    
    partner_name = fields.Char('Partner Name')
    order_id = fields.Char('Current Order')
    partner_credit_limit = fields.Float('Credit limit')
    partner_receivable = fields.Float('Total Receivable')
    due_after_current_order = fields.Float('Due after current quotation')
    is_hold = fields.Boolean('On Hold?')
    quotation_amount = fields.Float('Current Quotation Amount')
    exceeded_amount = fields.Float('Exceeded Amount')

    @api.model
    def default_get(self, fields):
        res = super(CreditLimitInfoWizard, self).default_get(fields)
        sale_order_id = self.env[self._context.get('active_model')].browse(self._context.get('active_id'))
        res.update({
            'partner_name': sale_order_id.partner_id.name,
            'order_id':sale_order_id.name,
            'partner_credit_limit':sale_order_id.partner_id.credit_limit_custom,
            'partner_receivable': sale_order_id.partner_id.credit,
            'due_after_current_order': sale_order_id.partner_id.credit + sale_order_id.amount_total,
            'is_hold': sale_order_id.partner_id.is_hold,
            'quotation_amount':sale_order_id.amount_total,
            'exceeded_amount':sale_order_id.partner_id.credit - sale_order_id.partner_id.credit_limit_custom + sale_order_id.amount_total
            })
        return res

    def action_confirm_order(self):
        sale_order_id = self.env[self._context.get('active_model')].browse(self._context.get('active_id'))
        template_id = self.env['ir.model.data']._xmlid_to_res_id('sr_customer_credit_limit.credit_limt_exceeded_email_template')
        if template_id:
            email_template_id = self.env['mail.template'].browse(template_id)
            order_url = str(self.env['ir.config_parameter'].sudo().get_param('web.base.url')) + "/web#id=" + str(sale_order_id.id) + "&view_type=form&model=sale.order"
            email_template_id.with_context(order_url=order_url, email_to=self.env['res.partner'].browse(SUPERUSER_ID).email).send_mail(sale_order_id.id, force_send=True)
        sale_order_id.with_context(confirm=True).action_confirm()
        return
    
