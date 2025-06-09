{
    'name':'sr_account_report_configuration',
    'description':'account report configuration',
    'version':'18.0.0.0',
    'depends':['base','account'],
    'data':[
        'security/ir.model.access.csv',
        'view/profit_loss_statement_view.xml',
        'view/financial_position_view.xml',
        'view/financial_statement_notes_view.xml',
        'view/aged_payables_summary_view.xml',
        'view/cash_flows_indirect_view.xml'
    ],
    'installable': True,
    'application': True,
    'license':  "LGPL-3"
}
