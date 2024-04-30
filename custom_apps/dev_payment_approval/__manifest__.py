# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Payment/Voucher Double Approval Workflow',
    'version': '11.0.1.0',
    'sequence': 1,
    'category': 'Accounting',
    'description':
        """
          This Module add below functionality into odoo

        1.Manager have to validate payments before Confirmation -- two or three step process
        2.This module helps you to set limit on Payments, So, Manager must have validate Payment if it exceed the Per-Defined Limit before Confirmation.
        3.Flow will be two step or three step based on conditions
        
        odoo payment approval 
        Odoo double payment approval
        odoo payment voucher approval 
        
    """,
    'summary': 'odoo app manage payment two three way approval process workflow',
    'depends': ['account_invoicing'],
    'data': [
        'security/security.xml',
        'views/view_res_config_settings.xml',
        'views/view_payment.xml',
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
    
    #author and support Details
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':25.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
