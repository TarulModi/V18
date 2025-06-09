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
    'name': 'Global Dynamic Excel Reports For all Application in Odoo',
    'version': '18.0.0.0',
    'category': 'Extra Addons',
    "license": "OPL-1",
    'summary': 'Global dynamic excel report dynamic export excel global dynamic excel export easy to export data in excel easy to generate excel report for all applications i.e Sales,purchase,invoices,CRM,payments, pickings, ETC ... ',
    'description': """
                dynamic excel report
                dynamic export in excel
                easy to export data in excel for all applications
                easy to generate excel report for all application
                generate dynamic excel report for all application
                dynamic global export excel report for modules
                export data in excel for all modules
                export data dynamically
                excel data export
                excel report generic
                excel report dynamic objects
                excel report with dynamic fields
                excel report with dynamic styles
                Business intelligence
                odoo BI
                odoo excel export,
                download excel report,
                accounting Reports
                generic export excel report,
                BI reporting
                dynamic excel export report,
                excel export report on Odoo,   
                Export data in Excel Reports 
""",
    "price": 10,
    "currency": 'EUR',
    'author': 'Sitaram',
    'depends': ['base'],
    'data': [
            'security/ir.model.access.csv',
             'views/sr_report_template.xml',
             'views/sr_global_dynamic_excel_report.xml',
             'wizards/sr_global_dynamic_excel_report.xml'
    ],
    'website':'https://sitaramsolutions.in',
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/WRRbUxIfu7g',
    "images":['static/description/banner.png'],
}
