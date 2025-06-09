# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################
from odoo import fields, api, models, _


class ProductCluster(models.Model):
    _name = 'partner.cluster'
    _description = 'Partner Cluster'

    name = fields.Char("Name")
    city = fields.Char("City")
    display_name = fields.Char("Ref", readonly='1')

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for rec in res:
            if rec.city:
                if len(rec.city) >= 3:
                    rec.display_name = rec.city[:3] + '_' + str(rec.id)
                elif len(rec.city) >= 1:
                    rec.display_name = rec.city + '_' + str(rec.id)
                else:
                    rec.display_name = ''
        return res

    def write(self, val):
        city = val.get('city')
        if city:
            if len(city) >= 3:
                val['display_name'] = city[:3] + '_' + str(self.id)
            elif len(city) >= 1:
                val['display_name'] = city + '_' + str(self.id)
            else:
                val['display_name'] = ''
        return super().write(val)
