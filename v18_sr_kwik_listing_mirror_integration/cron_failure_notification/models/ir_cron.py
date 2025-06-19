# -*- coding: utf-8 -*-
# ############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2025-TODAY Cybrosys Technologies(
#    <https://www.cybrosys.com>).
#    Author: MUHAMMED RISHAD (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import datetime
import logging
import time
from odoo import api, models, _
from odoo.exceptions import ValidationError
from odoo.fields import Datetime, _logger


class IrCron(models.Model):
    """ Inherits ir cron for add a feature that sends mail to admin
     each day, if any cron failed """
    _name = 'ir.cron'
    _inherit = ['ir.cron', 'mail.thread']


    def _callback(self, cron_name, server_action_id):
        """ Run the method associated to a given job. It takes care of logging
        and exception handling. Note that the user running the server action
        is the user calling this method. """
        self.ensure_one()
        print("----------cron_name------------",cron_name)
        print("----------server_action_id------------",server_action_id)
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
            _logger.info('Job %r (%s) done in %.3fs', cron_name, self.id,
                         end_time - start_time)
            if start_time and _logger.isEnabledFor(logging.DEBUG):
                _logger.debug('Job %r (%s) server action #%s with uid %s '
                              'executed in %.3fs',
                              cron_name, self.id, server_action_id,
                              self.env.uid, end_time - start_time)
            self.pool.signal_changes()
        except Exception as exception:
            self.pool.reset_changes()
            _logger.exception('Job %r (%s) server action #%s failed',
                              cron_name, self.id, server_action_id)
            # self.env.cr.rollback()
            print("----------exception------------", exception)
            if exception:
                self.env['failure.history'].create({
                    'name': cron_name,
                    'error': str(exception),
                })
            raise ValidationError(_(str(exception)))

    def mail_send_cron(self):
        """ If any cron's failed a notification email will send to admin """
        current_datetime = datetime.datetime.now()
        yesterday_datetime = current_datetime - datetime.timedelta(days=1)
        failure = self.env['failure.history'].search(
            [('create_date', '>', yesterday_datetime),
             ('create_date', '<', current_datetime)]
        )
        if failure:
            admin_mail = self.env['res.groups'].search(
                [('category_id', '=', 'Administration'),
                 ('name', '=', 'Access Rights')]).users.mapped('login')
            email_values = {
                'email_to': admin_mail[0] if len(admin_mail) == 1
                else ",".join(admin_mail)
            }
            mail_template = self.env.ref(
                'cron_failure_notification.mail_template_cron_error')
            mail_template.send_mail(self.id, email_values= email_values,
                                    force_send=True)
