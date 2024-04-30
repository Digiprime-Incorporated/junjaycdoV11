# -*- coding: utf-8 -*-

{
    'name': 'Skit PR Approval',
    'version': '1.1',
    'summary': 'Purchase Approval Flow',
    'author': 'Srikesh Infotech',
    'license': "AGPL-3",
    'website': 'http://www.srikeshinfotech.com',
    'description': """
        This module help to make multi level approval for purchase
    """,
    
    'category': "Purchase Management",
    'depends': ['base','hr'],

    "data": [
        "security/ir.model.access.csv",
        "views/skit_hr_employee.xml",
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}