# -*- coding: utf-8 -*-

import time
import logging
import datetime
from odoo import models, fields, api, _
from odoo.tools.translate import _
from odoo.exceptions import UserError


class LogsScheduledActions(models.Model):
    _description = "Error log"
    _name = 'logs.action'
    _inherit = ['mail.thread']

    user_id = fields.Many2one(
        'res.users', string="User", default=lambda self: self.env.user, index=True)
    name = fields.Char(string="Name", required=True, tracking=True)
    method = fields.Char(string="Method", tracking=True)
    created_by = fields.Many2one(
        'res.users', string="Created by", default=lambda self: self.env.user, index=True)
    object_action = fields.Char(string="Object", tracking=True)
    exec_date = fields.Datetime(string="Execution Date Time")
    company_name = fields.Many2one('res.company', string="Company",  default=lambda self: self.env.user.company_id,
                                   index=True)
    stages_id = fields.Selection(
        [('new', 'New'), ('confirm', 'Confirmed'), ('resolved', 'Resolved'), ('cancelled', 'Cancelled')], default='new')
    error_details = fields.Char(
        string="Error details", tracking=True)

    def action_mail_send(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        # template_id = ir_model_data._xmlid_to_res_id('app_script_cron_failure.scheduler_error_mailer')
        template_id = self.env.ref('app_script_cron_failure.scheduler_error_mailer', raise_if_not_found=False)

        try:
            compose_form_id = self.env.ref('mail.email_compose_message_wizard_form')
        except ValueError:
            compose_form_id = False
        # ctx = dict(
        #     'default_model'='logs.action',
        #     'default_res_ids'=self.ids,
        #     'default_template_id'=template_id,
        #     'default_composition_mode'='comment',
        # )

        ctx = dict(
                default_model='logs.action',
                default_res_ids=self.ids,
                default_template_id=template_id.id if template_id else False,
                default_composition_mode='comment',
                default_email_layout_xmlid="mail.mail_notification_light",
            )

        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id.id, 'form')],
            'view_id': compose_form_id.id,
            'target': 'new',
            'context': ctx,
        }

    def button_confirm_action(self):
        self.stages_id = 'confirm'

    def button_resolved_action(self):
        self.stages_id = 'resolved'

    def button_cancel_action(self):
        self.stages_id = 'cancelled'


_logger = logging.getLogger(__name__)


class IrCron(models.Model):
    _inherit = "ir.cron"

    # @api.model
    # def _handle_callback_exception(
    #         self, cron_name, server_action_id, job_id, job_exception):
    #     res = super(IrCron, self)._handle_callback_exception(
    #         cron_name, server_action_id, job_id, job_exception)
    #     my_cron = self.browse(job_id)
    #     print("----------my_cron--------",my_cron)
    #     self.env['logs.action'].create({
    #         'name': my_cron.name,
    #         'method': my_cron.model_id.name,
    #         'object_action': str(my_cron.code),
    #         'exec_date': datetime.datetime.now(),
    #         'error_details': str(job_exception),
    #     })
    #     print("----------res---res-----", res)
    #
    #     return res

    def _callback(self, cron_name, server_action_id):
        """ Run the method associated to a given job. It takes care of logging
        and exception handling. Note that the user running the server action
        is the user calling this method. """
        self.ensure_one()
        print("-----cron_name------11-----",cron_name)
        print("-----server_action_id--22---------",server_action_id)

        my_cron = self.browse(job_id)
        print("----------my_cron--------", my_cron)
        self.env['logs.action'].create({
            'name': my_cron.name,
            'method': my_cron.model_id.name,
            'object_action': str(my_cron.code),
            'exec_date': datetime.datetime.now(),
            'error_details': str(job_exception),
        })
        print("----------res---res-----", res)

        try:
            if self.pool != self.pool.check_signaling():
                # the registry has changed, reload self in the new registry
                self.env.reset()
                self = self.env()[self._name]

            _logger.debug(
                "cron.object.execute(%r, %d, '*', %r, %d)",
                self.env.cr.dbname,
                self._uid,
                cron_name,
                server_action_id,
            )
            _logger.info('Job %r (%s) starting', cron_name, self.id)
            start_time = time.time()
            self.env['ir.actions.server'].browse(server_action_id).run()
            self.env.flush_all()
            end_time = time.time()
            _logger.info('Job %r (%s) done in %.3fs', cron_name, self.id, end_time - start_time)
            if start_time and _logger.isEnabledFor(logging.DEBUG):
                _logger.debug('Job %r (%s) server action #%s with uid %s executed in %.3fs',
                              cron_name, self.id, server_action_id, self.env.uid, end_time - start_time)
            self.pool.signal_changes()
        except Exception:
            self.pool.reset_changes()
            print("-----cron_name----exceptionnnn-------",cron_name)
            _logger.exception('Job %r (%s) server action #%s failed', cron_name, self.id, server_action_id)
            self.env.cr.rollback()
            raise

    @api.model
    def test_scheduler_failure(self):
        """This function is used to test and debug this module"""
        pass

        # raise UserError(
        #     _("Task failure with UID = %d.") % self._uid)
