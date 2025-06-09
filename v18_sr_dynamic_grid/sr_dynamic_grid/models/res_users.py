from odoo import models, fields, api, SUPERUSER_ID

class Users(models.Model):
    _inherit = "res.users"

    def user_has_layout_access(self):
        return self.env.user._has_group('base.group_system')

    @classmethod
    def _login(cls, db, credential, user_agent_env):
        result = super()._login(db, credential, user_agent_env)
        if result.get('uid'):
            with cls.pool.cursor() as cr:
                self = api.Environment(cr, SUPERUSER_ID, {})[cls._name]
                user_layout_ids = self.env['user.layout'].sudo().search([
                    ('user_id', '=', result.get('uid')),
                    ('is_selected', '=', True)
                ])
                for user_layout_id in user_layout_ids:
                    user_layout_id.is_selected = False
        return result