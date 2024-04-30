
{
    'name': 'Web Export Tree View',
    'version': '11.0.2.0.0',
    'category': 'Web',
    'author': 'Digiprime Team',
    'website': 'www.digiprimeinc.com',
    'depends': [
        'web',
    ],
    "data": [
        'security/groups.xml',
        'views/web_export_view_view.xml',
    ],
    'qweb': [
        "static/src/xml/web_export_view_template.xml",
    ],

    'installable': True,
    'auto_install': False,
}
