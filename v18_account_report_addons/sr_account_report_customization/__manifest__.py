# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

{
    'name' : 'sr Account Report Customization',
    'description' : 'account report customization',
    'version' : '18.0.0.0',
    'depends' : ['base','account','sr_account_report_configuration',],
    'data' : [
        'reports/profit_loss_statement_report_view.xml',
        # 'reports/financial_statemnt_action.xml',
        # 'reports/action_report_financial_position.xml',
        # 'reports/action_report_profit_loss_statement.xml',
        'reports/cash_flow_report.xml',
        'reports/aged_payable_report_template.xml',
        'reports/financial_statement_notes_report.xml',
        'reports/financial_position_report_view.xml',
        'view/menu_view.xml',

    ],
    'installable' : True,
    'application' : True,
    'license' : 'LGPL-3',
}
