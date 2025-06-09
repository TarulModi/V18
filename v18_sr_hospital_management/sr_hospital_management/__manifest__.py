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
    "name": "Hospital Management System",
    "version": "18.0.0.0",
    "category": "Healthcare",
    "summary": "",
    "description": """
    """,
    "author": "Sitaram",
    "depends": ["base", "contacts", "hr", 'mail', 'resource'],
    "data": [
        "security/ir.model.access.csv",
        #"security/sr_hospital_config_group.xml",
        'data/ir_sequence_data.xml',
        "views/menu_view.xml",
        "views/room_facility_view.xml",
        "views/bed_view.xml",
        "views/room_type_view.xml",
        "views/ward_view.xml",
        "views/room_view.xml",
        "views/res_partner_view.xml",
        "views/hospital_specialization_view.xml",
        "views/hr_employee_doctor_view.xml",
        "views/hr_employee_staff_view.xml",
        "views/hr_department_view.xml",
        "views/hr_job_position_view.xml",
        "views/hospital_appointment_view.xml",
        "views/hospital_ipd_admission_view.xml",
        "views/resource_calendar_view.xml",
        "views/diseases_type_view.xml",
        "views/diseases_view.xml",
    ],
    "website": "https://sitaramsolutions.in",
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "OPL-1",
}

