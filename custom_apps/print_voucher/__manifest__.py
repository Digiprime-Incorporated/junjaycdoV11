# -*- coding: utf-8 -*-
# Copyright (C)2017 -present Technaureus Info Solutions(<http://technaureus.com/>).

{
    'name': 'Receipt and Payment Voucher Print(Payment Receipt)',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 1,
    'summary': 'Receipt and Payment Voucher Print(Payment Receipt).',
    'description': """
This module helps to print receipt and payment voucher with both customer/vendor copy and office copy.
Also it automatically loads the sub currency of each country and which in turn helps to show the amount in words. 
    """,
    'website': 'http://technaureus.com/',
    'author': 'Technaureus Info Solutions',
    'depends': ['account_voucher'],
    'price': 22,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'data': [
        'report/layout.xml',
        'report/report_header.xml',
        'report/report_footer.xml',
        'report/account_report.xml',
        'report/report_voucher.xml',
    ],
    'demo': [],
    'css': [],
    'images': ['images/receipt_payment_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
