/** @odoo-module **/

import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";
import { EventBus } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

var inactivityTimeout = Date.now();
let activityTimer = null;
const activityKey = 'userActivity';

export const sessionTimeoutService = {
    async start(env) {
        const bus = new EventBus();
        const resetInactivityTimer = async () => {
                if (activityTimer) {
                    clearTimeout(activityTimer);
                }
                await rpc('/session_timeout', {})
                .then(function (result) {
                    if (result.session_timeout_date) {
                        inactivityTimeout = result.session_timeout_date
                    }
                });

                var today = new Date().toISOString().split('T')[0]
                browser.localStorage.setItem(activityKey, today);
                if (inactivityTimeout && inactivityTimeout < today) {
                    activityTimer = setTimeout(logoutUser, 300);
                }
            }
        const logoutUser = () => {
            rpc('/fetch_logout_url', {})
                .then(function (logout_url) {
                    if (logout_url) {
                        browser.localStorage.setItem('logout_url', logout_url);
                        if (browser.localStorage.getItem('logout_url') && browser.localStorage.getItem('logout_url') !== "false") {
                            var logout_url = browser.localStorage.getItem('logout_url');
                            browser.localStorage.setItem('logout_url', "false");
                            window.location.href = logout_url;
                        }
                        else
                        {
                            rpc('/fetch_logout_url', {})
                                .then(function (logout_url) {
                                    if (logout_url) {
                                        browser.localStorage.setItem('logout_url', logout_url);
                                    }
                            });
                            var logout_url = browser.localStorage.getItem('logout_url');
                            browser.localStorage.setItem('logout_url', "false");
                            window.location.href = logout_url;
                        }
                    }
                });
            }

        const startSessionMonitor = () => {
            resetInactivityTimer();
            ['mousemove', 'keydown', 'touchstart'].forEach(function (eventType) {
                window.addEventListener(eventType, resetInactivityTimer);
            });
        }

        await rpc('/session_timeout', {})
            .then(function (result) {
                if (result.session_timeout_date) {
                    inactivityTimeout = result.session_timeout_date
                    startSessionMonitor();
                }
            });

        window.addEventListener('load', function () {
            if (browser.localStorage.getItem('logout_url') && browser.localStorage.getItem('logout_url') !== "false") {
               var logout_url = browser.localStorage.getItem('logout_url');
               browser.localStorage.setItem('logout_url', "false");
               window.location.href = logout_url;
            }
        });
        return {
            bus
        };
    },
};

registry.category("services").add("web_client_ready", sessionTimeoutService);
