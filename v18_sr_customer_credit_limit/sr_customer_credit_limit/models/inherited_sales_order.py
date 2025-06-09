# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import RedirectWarning, UserError


class SalesOrder(models.Model):
    _inherit = "sale.order"
    
    customer_receivable_amount = fields.Monetary(string="Total Receivable", related="partner_id.credit")
    customer_credit_limit = fields.Float(string="Credit Limit", related="partner_id.credit_limit_custom")
    is_warning = fields.Boolean('Show Warning')

    @api.model
    def create(self, vals):
        result = super(SalesOrder, self).create(vals)
        if result.partner_id.credit_check and result.partner_id.blocking_limit != 0.0:
            if (result.partner_id.credit - result.partner_id.debit) > result.partner_id.blocking_limit:
                raise UserError(_('The Customer is in blocking stage and has to pay ' + str(result.partner_id.credit - result.partner_id.debit)))
        return result

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            if self.partner_id.credit_check and self.partner_id.is_hold:
                # return {'RedirectWarning': {'title': "Credit Limit On Hold", 'message':"Customer '" + self.partner_id.name + "' is on credit limit hold due to exceeding your credit limit. Please contact administration for further guidance." } }
                return {'warning': {'title': "Credit Limit On Hold", 'message':"Customer '" + self.partner_id.name + "' is on credit limit hold due to exceeding your credit limit. Please contact administration for further guidance." } }
            if self.partner_id.credit_check and (self.partner_id.credit - self.partner_id.debit) > self.partner_id.credit_limit_custom:
                self.is_warning = True

    def action_confirm(self):
        if self._context.get('confirm'):
            return super(SalesOrder, self).action_confirm()
        if self.partner_id.credit_check:
            if self.partner_id.is_hold:
                raise UserError(_('You have been put on hold due to exceeding your credit limit. Please contact administration for further guidance.'))
            else:
                total_amount = self.customer_receivable_amount - self.partner_id.debit + self.amount_total
                if total_amount >= self.partner_id.credit_limit_custom:
                    wizard_credit_limit_form_id = self.env.ref('sr_customer_credit_limit.view_customer_credit_information_wizard_form')
                    if wizard_credit_limit_form_id:
                        res = {
                            'name' : _('Credit Limit Exceed View'),
                            'type' : 'ir.actions.act_window',
                            'view_type' : 'form',
                            'view_mode' : 'form',
                            'res_model' : 'credit.limit.wizard',
                            'view_id' : wizard_credit_limit_form_id.id,
                            'target' : 'new',
                        }
                        return res 
                    else:
                        raise UserError(_('Credit Limit Exceed View Not Found. \n Please Update Our Module and Try Again..!'))
                else:
                    return super(SalesOrder, self).action_confirm()
        else:
            return super(SalesOrder, self).action_confirm()
