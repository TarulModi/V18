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


class ClassSubject(models.Model):
    _name = "class.subject"
    _inherit = ['mail.thread']
    _description = "Class Subject"
    _rec_name = "subject_id"

    class_room_id = fields.Many2one("class.room", string="Class Room", tracking=True)
    subject_id = fields.Many2one("subject.subject", string="Subject", tracking=True)