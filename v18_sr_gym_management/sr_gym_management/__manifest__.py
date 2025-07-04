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
    "name": "GYM Management",
    "version": "18.0.0.0",
    "category": "Hidden",
    "license": "OPL-1",
    "summary": "GYM Management",
    "description": """
        GYM Management
    """,
    "depends": ["base", "mail", "snailmail", "hr", "account"],
    "data": [
        #"security/education_security.xml",
        "security/ir.model.access.csv",
        #"data/ir_sequence_data.xml",
        "views/menu_view.xml",
        "views/trainer_skills_view.xml",
        "views/diet_interval_view.xml",
        "views/body_parts_view.xml",
        "views/workout_days_view.xml",
        "views/gym_membership_view.xml",
        "views/product_template_view.xml",
        "views/hr_employee_views.xml",
        "views/res_partner_views.xml",
        "views/bmi_calculation_view.xml",
        "views/exercise_for_view.xml",
        "views/gym_exercise_view.xml",
        "views/gym_workout_view.xml",
        "wizard/buy_membership_wizard_view.xml",
    ],
    "price": 10,
    "currency": "EUR",
    "author": "Sitaram",
    "installable": True,
    "auto_install": False,
    "application": True,
    "website": "https://www.sitaramsolutions.in",
    "live_test_url": "https://www.sitaramsolutions.in",
    "images": ['static/description/banner.png'],
}
