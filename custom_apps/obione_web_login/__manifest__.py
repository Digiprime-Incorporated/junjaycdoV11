{
    'name': 'Briq Web Login Screen',
    'summary': 'Customize Briq Web Login Screen',
    'version': '12.0.0.0',
    'category': 'Website',
    'summary': """
New Odoo Login Screen
""",
    'author': "Elms (www.digiprime.com)",
    'website': 'http://www.digiprim.com',
    'license': 'AGPL-3',
    'depends': [
    ],
    'data': [
        'data/ir_config_parameter.xml',
        'templates/website_templates.xml',
        'templates/webclient_templates.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
}
