# -*- coding: utf-8 -*-
{
    'name': "my_office_automation",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Alireza Qomi",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
        'depends': [
        'base',
        'hr',
        'mail',
    ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/send_massage.xml',
        'views/resive_massage.xml',
        'views/company_message_views.xml',
        'views/company_message_views_forward.xml',
        'views/menu.xml',

    ],
    
    'assets': {
        'web.assets_backend': [
            'my_office_automation/static/src/js/mark_read.js',
        ],
    },


    # only loaded in demonstration mode

    'installable': True,
    'application': True,
}

