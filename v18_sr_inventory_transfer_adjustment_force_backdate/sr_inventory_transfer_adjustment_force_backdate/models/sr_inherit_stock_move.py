# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, models
from datetime import date


class srStockMove(models.Model):
    _inherit = 'stock.move'
    
    def _action_done(self, cancel_backorder=False):
        res = super(srStockMove, self)._action_done()
        if res.picking_id and res.picking_id.force_back_date or self._context.get('force_back_date'):
            for move in res:
                if move.picking_id:
                    force_date = move.picking_id.force_back_date
                elif self._context.get('force_back_date'):
                    force_date = self._context.get('force_back_date')
                else:
                    force_date = date.today()
                move.write({'date':force_date})
                for move_line in move.move_line_ids:
                    move_line.write({'date':force_date})
                for svl in move.stock_valuation_layer_ids:
                    self._cr.execute("update stock_valuation_layer set create_date = %s where id = %s", [force_date, svl.id])
        return res

    def _prepare_account_move_vals(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id,
                                   cost):
        self.ensure_one()
        valuation_partner_id = self._get_partner_id_for_valuation_lines()
        move_ids = self._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id, svl_id, description)
        svl = self.env['stock.valuation.layer'].browse(svl_id)

        # Base code
        # if self.env.context.get('force_period_date'):
        #     date = self.env.context.get('force_period_date')
        # elif svl.account_move_line_id:
        #     date = svl.account_move_line_id.date
        # else:
        #     date = fields.Date.context_today(self)

       # Changes code
        if self.picking_id.force_back_date:
            date = self.picking_id.force_back_date
        elif self._context.get('force_back_date'):
            date = self._context.get('force_back_date')
        else:
            date = self._context.get('force_period_date', fields.Date.context_today(self))

        return {
            'journal_id': journal_id,
            'line_ids': move_ids,
            'partner_id': valuation_partner_id,
            'date': date,
            'ref': description,
            'stock_move_id': self.id,
            'stock_valuation_layer_ids': [(6, None, [svl_id])],
            'move_type': 'entry',
            'is_storno': self.env.context.get('is_returned') and self.company_id.account_storno,
            'company_id': self.company_id.id,
        }
