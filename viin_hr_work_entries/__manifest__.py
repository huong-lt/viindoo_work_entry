# -*- coding: utf-8 -*-
{
    'name': "Viin Work Entries",
    'name_vi_VN': "Nhật ký công việc",

    'summary': """
        Manage work entry of employee""",
    'summary_vi_VN': """
        Quản lý công việc của nhân viên
        """,    

    'description': """
What is does
============
This module is managing work entry of employee

Editions Supported
==================
1. Community Edition
2. Enterprise Edition
    """,

    'description_vi_VN': """
Module này làm gì
=================
Module này quản lý công việc của nhân viên.

Ấn bản được Hỗ trợ
==================
1. Ấn bản Community
2. Ấn bản Enterprise
    """,

    'author': "Viindoo",
    'website': "https://viindoo.com",
    'live_test_url': "https://v15demo-int.viindoo.com",
    'live_test_url_vi_VN': "https://v15demo-vn.viindoo.com",
    'support': "apps.support@viindoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'HR',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','viin_hr','hr_work_entry', 'hr_work_entry_contract'],
    
    # always loaded
    'data': [
        'security/hr_work_entry_security.xml',
        'security/ir.model.access.csv',
        'views/main_menu.xml',
        'views/templates.xml',
        'views/viin_hr_work_entry_views.xml',
        'reports/viin_hr_work_entry_report.xml',
        'views/res_config_settings_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images' : ['static/description/main_screenshot.png'],
    'application': True,
}
