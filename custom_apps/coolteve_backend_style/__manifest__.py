# -*- coding: utf-8 -*-
{
    'name': "CooLTEve Backend Style",

    'summary': """
        Odoo + AdminLTE + LOVE = CooLTEve """,

    'description': """
        Odoo + AdminLTE + LOVE = CooLTEve
    """,

    'author': "Tepat Guna Karya",
    'website': "http://www.tepatguna.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Themes/Backend',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/ir_config_parameter.xml',
        'views/assets.xml',
        'views/coolteve_backend_style_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # 'qweb': ['static/src/xml/base.xml'],
    'installable': True,
    'application': True,
    'price': 30,
    'currency': 'EUR',
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
}
