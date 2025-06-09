from odoo import models, fields, api

class GridLayoutTemplate(models.Model):
    _name = 'grid.layout.template'
    _description = 'Grid Layout Template'

    name = fields.Char(string='Template Name', required=True)
    user_ids = fields.Many2many('res.users', string='View Users')
    view_id = fields.Many2one('ir.ui.view', string='View', required=False)
    layout = fields.Text(string='Layout')

    def update_layout_id(self):
        selected_user_layout_ids = self.env['user.layout'].search([('user_id', '=', self.env.user.id),
                                                                   ('layout_id.view_id', '=', self.view_id.id),
                                                                   ('is_selected', '=', True)])
        for selected_user_layout_id in selected_user_layout_ids:
            selected_user_layout_id.is_selected = False

        selected_user_layout_id = self.env['user.layout'].search([('user_id', '=', self.env.user.id),
                                                                   ('layout_id', '=', self.id)],limit=1)
        selected_user_layout_id.is_selected = True

    def update_current_user_layout(self):
        self.ensure_one()
        exits_layout_ids = self.env['user.layout'].search([('layout_id', '=', self.id)])
        exits_layout_ids.sudo().unlink()
        for user in self.user_ids:
            user_layout_data = {
                'user_id' : user.id,
                'layout_id' : self.id,
            }
            if self.env.user == user:
                selected_user_layout_ids = self.env['user.layout'].search([('user_id','=',user.id),
                                                ('layout_id.view_id','=',self.view_id.id),
                                                ('is_selected','=',True)])
                for selected_user_layout_id in selected_user_layout_ids:
                    selected_user_layout_id.is_selected = False
                user_layout_data.update({'is_selected' : True})

            self.env['user.layout'].create(user_layout_data)

    @api.model_create_multi
    def create(self,vals):
        res = super(GridLayoutTemplate, self).create(vals)
        res.update_current_user_layout()
        return res

    def write(self,vals):
        res = super(GridLayoutTemplate, self).write(vals)
        self.update_current_user_layout()
        return res

    def unlink(self):
        for rec in self:
            self.env['user.layout'].search([('layout_id','=',rec.id)]).sudo().unlink()
        return super(GridLayoutTemplate, self).unlink()
