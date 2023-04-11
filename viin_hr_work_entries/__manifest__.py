# -*- coding: utf-8 -*-
{
    'name': "Viin Work Entries",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','viin_hr','hr_work_entry'],

    # always loaded
    'data': [
        'security/hr_work_entry_security.xml',
        'security/ir.model.access.csv',
        'views/main_menu.xml',
        'views/templates.xml',
        'views/viin_hr_work_entry_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
     'application': True,
}