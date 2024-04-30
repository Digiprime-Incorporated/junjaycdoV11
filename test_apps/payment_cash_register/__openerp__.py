# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt. Ltd. See LICENSE file for full copyright and licensing details.

{
    'name':'Cash Register On Payment',
    'version':'1.0',
    'category':'Accounting & Finance',
    'price': 80.0,
    'currency': 'EUR',
    'summary': 'Cash Register Selection on Payment Forms.',
    'license': 'Other proprietary',
    'description': """
                Payment Cash Register:
This module added features on customer/supplier payments to allow account user to link payment with cash register direct through payment menu or customer/supplier invoices register payment option. After selecting and validating payment, module will add cash register line on selected cash register.

Features are:

User can select cash register through Payments menus.
User can select cash register while they are on customer invoices menu and make payment through select register payment option.

Tags
- cash register payment
- customer payment with cash register
- supplier payment with cash register
- register payment with cash register
cash register on customer payment
cash register on supplier payment
cash register on payment
payment with cash register
cash on payment
select cash register on payment
select register on payment
select cash note in payment
            """,
    'author': "Probuse Consulting Service Pvt. Ltd.",
    'website': "http://www.probuse.com",
    'depends': ['account'],
    'data':[
            'views/payment_cash_register.xml',
            ],
    'installable': True,
    'application': False,
}
 
