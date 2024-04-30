# -*- coding: utf-8 -*-
{
    'name': 'Print Barcode in sales, purchase, inventory, accounts, and mrp reports.',

    'author' : 'Softhealer Technologies',
    
    'website': 'https://www.softhealer.com',    
    
    'version': '11.0.1',
    
    'category': 'Extra Tools',
    
    'summary': 'This module use to show barcode in sale order reports, purchase order reports, inventory reports, accounting reports and mrp reports.',
    
    'description': """Barcodes eliminate the possibility of human error. The occurrence of errors for manually entered data is significantly higher than that of barcodes. A barcode scan is fast and reliable, and takes infinitely less time than entering data by hand. 
    This module use to show barcode in sale order reports, purchase order reports, warehouse reports, accounting reports and mrp reports. Very useful to make process faster, Quickly read sale order, purchase order, invoice, bills, delivery order, picking operation, mrp order no by barcode scanner.""",
    
    'depends': ['product','barcodes','purchase','sale_management','stock','mrp','account'], 
    
    'data': [
        'reports/sale_order_report.xml',        
        'reports/purchase_order_report.xml',        
        'reports/account_invoice_report.xml',        
        'reports/stock_delivery_slip_report.xml',
        'reports/manufacturing_report.xml',                
    ],    
    'images': ['static/description/background.png',],            
    
    'installable': True,
    'auto_install': False,
    'application': True,    
    "price": 18,
    "currency": "EUR"        
}
