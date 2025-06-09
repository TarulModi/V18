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

class ProjectTask(models.Model):
    _inherit = 'project.task'

    product_ids = fields.Many2many('product.product',string="product")
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')

    def action_show_sale_order(self):
        self.ensure_one()
        return {
            'name': _("Related Quotation/Sales Order"),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'view_id': False,
            'res_id': self.sale_order_id.id,
            'type': 'ir.actions.act_window',
        }