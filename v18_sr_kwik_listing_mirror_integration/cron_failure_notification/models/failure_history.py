# -*- coding: utf-8 -*-
##############################################################################
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
from odoo import fields, models


class FailureHistory(models.Model):
    """Creates failure history to store the failed cron action details
        as a record"""
    _name = 'failure.history'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Failure History'

    name = fields.Char(string='Name', required=True, help="Failed cron action "
                                                          "name")
    error = fields.Char(string='Error Details', help="Detailed description "
                                                     "about error")
