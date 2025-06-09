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


class SaleConfigurationSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    so_sale_allow = fields.Boolean('Allow Convert Sales Order')
    so_sent_allow = fields.Boolean('Allow Convert Quotation Sent')
    so_draft_allow = fields.Boolean('Allow Convert Quotation')

    @api.model
    def get_values(self):
        res = super().get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            so_draft_allow=params.get_param('sr_so_convert_task.so_draft_allow', default=False),
            so_sent_allow=params.get_param('sr_so_convert_task.so_sent_allow', default=False),
            so_sale_allow=params.get_param('sr_so_convert_task.so_sale_allow', default=False),
        )
        return res

    def set_values(self):
        super().set_values()
        config = self.env['ir.config_parameter'].sudo()
        config.set_param('sr_so_convert_task.so_draft_allow', self.so_draft_allow)
        config.set_param('sr_so_convert_task.so_sent_allow', self.so_sent_allow)
        config.set_param('sr_so_convert_task.so_sale_allow', self.so_sale_allow)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    task_id = fields.Many2one('project.task', string="Task", readonly=True)
    convert = fields.Boolean(string="Convert SO to Task", compute='_compute_convert_task')

    @api.depends('state')
    def _compute_convert_task(self):
        # Use sudoed config parameters for public access
        config_params = self.env['ir.config_parameter'].sudo()
        for order in self:
            allow_convert = config_params.get_param(f'sr_so_convert_task.so_{order.state}_allow', default='False')
            order.convert = allow_convert == 'True'

    def action_show_task(self):
        self.ensure_one()
        return {
            'name': _("Related Task"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.task',
            'res_id': self.task_id.id,
        }


class SoConvertTask(models.TransientModel):
    _name = 'so.convert.task'
    _description = 'SO Convert to Task Wizard'

    project_id = fields.Many2one('project.project', string='Select Project', required=True)
    stage_id = fields.Many2one('project.task.type', string='Select Stage', required=True)

    def create_task(self):
        sale_order = self.env['sale.order'].browse(self._context.get('active_id'))
        task_vals = {
            'project_id': self.project_id.id,
            'stage_id': self.stage_id.id,
            'date_deadline': sale_order.validity_date,
            'name': sale_order.name,
            'product_ids': [(6, 0, sale_order.order_line.mapped('product_id').ids)],
            'partner_id': sale_order.partner_id.id,
            # 'user_id': sale_order.user_id.id,
            'description': sale_order.note,
            'sale_order_id': sale_order.id,
        }
        task = self.env['project.task'].create(task_vals)
        sale_order.task_id = task.id
