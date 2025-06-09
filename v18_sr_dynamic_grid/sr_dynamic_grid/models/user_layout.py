from odoo import models,fields,api

class UserLayout(models.Model):
    _name = "user.layout"
    _description = "User Layout"

    user_id = fields.Many2one('res.users', string='User', required=True)
    layout_id = fields.Many2one('grid.layout.template', string='Layout Template', required=True)
    is_selected = fields.Boolean(string='Is Selected',default=False)