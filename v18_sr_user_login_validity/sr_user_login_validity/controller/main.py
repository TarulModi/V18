# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

import werkzeug
from odoo import http
from odoo.http import request
from datetime import datetime
from odoo.addons.web.controllers.home import Home


class srHome(Home):
    @http.route()
    def web_login(self, redirect=None, **kw):
        login = kw.get("login")
        res_user = (
            request.env["res.users"]
            .sudo()
            .search([("login", "=", login)])
        )
        if not res_user.user_time_validity:
            return super(srHome, self).web_login(redirect=redirect, **kw)

        current_date = datetime.now().date()
        start_date = res_user.start_date
        end_date = res_user.end_date

        if not (start_date < current_date and current_date > end_date):
            return super(srHome, self).web_login(redirect=redirect, **kw)
        else:
            return werkzeug.utils.redirect("/web/login?error=%s" % (res_user.message))

class SessionTimeoutController(http.Controller):

    @http.route('/session_timeout', type='json', auth='user')
    def session_timeout(self):
        user_settings_date = request.env.user.end_date if request.env.user.user_time_validity else False
        return {'session_timeout_date': user_settings_date}

    @http.route('/fetch_logout_url', type='json', auth='user')
    def fetch_logout_url(self):
        logout_url = "/web/session/logout"
        if request.env.user:
            logout_url = '/web/session/logout?redirect=/web/login'
        return logout_url
