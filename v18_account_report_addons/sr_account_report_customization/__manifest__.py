{
    'name' : 'sr_account_report_customization',
    'description' : 'account report customization',
    'version' : '18.0.0.0',
    'depends' : ['base','account','sr_account_report_configuration',],
    'data' : [
        'reports/action_report_profit_loss_statement.xml',
        'reports/profit_loss_statement_report_view.xml',
        'reports/financial_statemnt_action.xml',
        'reports/financial_statement_notes_report.xml',
        'reports/aged_payable_report_template.xml',
        'view/menu_view.xml',
    ],
    'installable' : True,
    'application' : True,
    'license' : 'LGPL-3',

}
