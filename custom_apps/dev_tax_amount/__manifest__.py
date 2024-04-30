 # -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Devintelle Solutions (<http://devintellecs.com/>).
#
##############################################################################

{
    'name': 'Tax Amount-Sale,Purchase,Invoice',
    'version': '1.0',
    'category': 'sale',
    'sequence':1,
    'summary': 'Apps will Addd tax amount and total with tax in Sale, Purchase and Invoice lines.',
    'description': """
                Apps will Addd tax amount and total with tax in Sale, Purchase and Invoice lines 
 """,
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com/',
    'depends': ['sale','purchase','account'],
    'data': [
        'views/tax_sale_view.xml',
        'views/tax_purchase_view.xml',
        'views/tax_invoice_view.xml',
    ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price':15.0,
    'currency':'EUR',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
