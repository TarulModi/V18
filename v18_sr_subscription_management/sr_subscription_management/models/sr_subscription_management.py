# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from _datetime import datetime
from odoo import api, fields, models, _


class srSubscriptionManagement(models.Model):
    _name = "sr.subscription.management"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Subscription Management"

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].sudo().search([])
        return [(model.model, model.name)
                for model in models
                ]

    name = fields.Char(string='Subscription Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    date = fields.Date(string='Subscription date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)]}, copy=False, default=fields.Date.context_today, track_visibility='always', track_sequence=1)
    company_id = fields.Many2one('res.company', 'Company', readonly=True, default=lambda self: self.env['res.company']._company_default_get('sr.subscription.management'))
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user, readonly=True)
    interval_number = fields.Integer(string='Times of Interval', default=1)
    reference = fields.Reference(string='Related Document',selection='_reference_models')
    interval_type = fields.Selection([('minutes', 'Minutes'), ('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months')], string='Interval Unit', default='months')
    nextcall = fields.Datetime(string='Next Execution Date', default=fields.Datetime.now, index=True, track_visibility='always', track_sequence=2)
    cron_id = fields.Many2one('ir.cron', string='Cron Reference', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('running', 'Running'), ('done', 'Done')], 'Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3, default='draft')
    note = fields.Text(string='Notes')
    number_of_call = fields.Integer('Number Of Subscription')
    subscription_document_history_ids = fields.One2many('sr.subscription.document.history', 'subscription_id', string="Subscription Document History")

    # @api.model
    # def create(self, vals):
    #     # if vals.get('name', _('New')) == _('New'):
        #     if 'company_id' in vals:
        #         vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('sr.subscription.management') or _('New')
        #     else:
        #         vals['name'] = self.env['ir.sequence'].next_by_code('sr.subscription.management') or _('New')
        #
    #     result = super(srSubscriptionManagement, self).create(vals)
    #     return result

    @api.model_create_multi
    def create(self, vals):
        if isinstance(vals, list):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'sr.subscription.management') or _('New')
            else:
                for val in vals:
                    if val.get('name', _('New')) == _('New'):
                        val['name'] = self.env['ir.sequence'].next_by_code('sr.subscription.management') or _('New')
        else:
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('sr.subscription.management') or _('New')
            else:
                if vals.get('name', _('New')) == _('New'):
                    vals['name'] = self.env['ir.sequence'].next_by_code('sr.subscription.management') or _('New')

        result = super(srSubscriptionManagement, self).create(vals)
        return result

    def start_subscription(self):
        model_subscription = self.env.ref('sr_subscription_management.model_sr_subscription_management')
        if not self.cron_id:
            cron_obj = self.env['ir.cron']
            cron_id = cron_obj.create({
                'name': self.name,
                'model_id': model_subscription.id,
                'state': 'code',
                'user_id': self.user_id.id,
                'interval_number': self.interval_number,
                'interval_type': self.interval_type,
                'nextcall': self.nextcall,
                # 'numbercall': self.number_of_call,
                'code': 'model.perform_subscription(' + str(self.id) + ')',
            })
            if cron_id:
                self.update({'cron_id': cron_id.id, 'state': 'running'})
        else:
            self.cron_id.update(
                {
                'name': self.name,
                'model_id': model_subscription.id,
                'state': 'code',
                'user_id': self.user_id.id,
                'interval_number': self.interval_number,
                'interval_type': self.interval_type,
                'nextcall': self.nextcall,
                # 'numbercall': self.number_of_call,
                'code': 'model.perform_subscription(' + str(self.id) + ')',
            })
            self.update({'state': 'running'})
            
        return True
    
    def stop_subscription(self):
        self.update({'state': 'done'})
        self.cron_id.active = False

    def set_to_draft(self):
        self.cron_id.active = True
        self.state = 'draft'

    @api.onchange('state')
    def onchange_state(self):
        if self.state == 'done':
            self.cron_id.active = False
    
    def perform_subscription(self, subscription_id):
        subscription_browse_id = self.env['sr.subscription.management'].browse(subscription_id)
        document_id = subscription_browse_id.reference.id
        document_model = subscription_browse_id.reference._name
        subscription_document = self.env[document_model].browse(document_id).copy()
        self.env['sr.subscription.document.history'].create({
            'date': datetime.now(),
            'subscription_id':subscription_id,
            'document_id':document_model + ',' + str(subscription_document.id)
            })
        # if subscription_browse_id.cron_id.numbercall == 1:
        if subscription_browse_id.number_of_call == 1:
            subscription_browse_id.update({'state': 'done'})


class srSubscriptionDocumentHistory(models.Model):
    _name = 'sr.subscription.document.history'
    _description = "Subscription Document History"
    _rec_name = 'date'
 
    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].sudo().search([])
        return [(model.model, model.name)
                for model in models
                ]
 
    date = fields.Datetime('Date')
    subscription_id = fields.Many2one('sr.subscription.management', 'Subscription', ondelete='cascade')
    document_id = fields.Reference(string='Document', selection=_reference_models)
