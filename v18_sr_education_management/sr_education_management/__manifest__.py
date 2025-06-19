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
    "name": "Education Management",
    "version": "18.0.0.0",
    "category": "Hidden",
    "license": "OPL-1",
    "summary": "Education Management",
    "description": """
        Education Management
    """,
    "depends": ["base", "mail", "snailmail", "hr", "accountant"],
    "data": [
        "security/education_security.xml",
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/school_configurations.xml",
        "views/language_view.xml",
        "views/religions_view.xml",
        "views/term_structure_view.xml",
        "views/academic_year_view.xml",
        "views/notice_boards_view.xml",
        "views/mother_tongue_view.xml",
        "views/division_view.xml",
        "views/hobby_view.xml",
        "views/grade_view.xml",
        "views/subject_view.xml",
        "views/courses_view.xml",
        "views/student_view.xml",
        # "views/medium_view.xml",
        "views/class_room_view.xml",
        "views/admission_view.xml",
        "views/inherited_hr_employee.xml",
        "views/inherited_departments_view.xml",
        "views/timetable_view.xml",
        "views/fees_structure_view.xml",
        # "wizard/admission_doc_varification.xml",
        "wizard/bulk_enroll_assign.xml",
        "wizard/doc_preview.xml"
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




