# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError


class srMassConfirmPicking(models.TransientModel):
    _name = 'mass.confirm.picking'
    _description = "Mass Confirm Picking"

    picking_ids = fields.Many2many('stock.picking',string="Pickings")

    @api.model
    def default_get(self,fields):
        res = super(srMassConfirmPicking, self).default_get(fields)
        picking_ids = []
        sms_confirmation = self.env.company.stock_move_sms_validation
        if sms_confirmation:
            raise UserError(_('Please Disable SMS Confirmation\nGo to Inventory -> Configuration -> Settings -> Turn off SMS Confirmation'))
        if any(record.state!='sale' for record in self.env['sale.order'].browse(self._context.get('active_ids'))):
               raise UserError(_('Some of selected sales order are not in confirm state \n Please confirm then validate the picking'))
        for record in self.env['sale.order'].browse(self._context.get('active_ids')):
            for picking in record.picking_ids:
                picking_ids.append(picking.id)
        res['picking_ids']=[(6,0, picking_ids)]
        return res
    
    def sr_mass_confirm_picking(self):
        for record in self.picking_ids:
            if record.state == 'assigned':
                for line in record.move_ids_without_package:
                    line.write({'quantity':line.product_uom_qty})
                record.button_validate()
