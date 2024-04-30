# -*- coding: utf-8 -*-

# Created on 2018-11-05
# author: 广州尚鹏，http://www.sunpop.cn
# email: 300883@qq.com
# resource of Sunpop
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# Odoo在线中文用户手册（长期更新）
# http://www.sunpop.cn/documentation/user/10.0/zh_CN/index.html

# Odoo10离线中文用户手册下载
# http://www.sunpop.cn/odoo10_user_manual_document_offline/
# Odoo10离线开发手册下载-含python教程，jquery参考，Jinja2模板，PostgresSQL参考（odoo开发必备）
# http://www.sunpop.cn/odoo10_developer_document_offline/
# description:
{
    'name': 'App Product Auto Code by Category, Variants Supported',
    'summary': 'Best Product Auto code. Variants Supported. Auto Default Attributes. Unique code. Customize Sequence for each category. like [raw-ipad-001],[raw-ipad-002]',
    "version": '11.0.11.1',
    'category': 'Sales',
    'author': 'Sunpop.cn',
    'website': 'http://www.sunpop.cn',
    'license': 'AGPL-3',
    'sequence': 2,
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/set2.jpg'],
    'currency': 'EUR',
    'price': 68,
    'description': """
        Best Product Auto code. Variants Supported. Auto Default Attributes. Unique code. Auto reference, unique reference.
            
        This module allows to associate a sequence to the product reference by category.
        The reference (default code) is unique (SQL constraint) and required.
        Support Product with or without Variants.
        1. Auto code for every Product and Product Variants.自动产品编码。
        2. Get different sequence for different category.不同产品目录生成不同产品编码。
        3. Auto Code for every product variants, like product20181130-001.自动多规格产品编码，形式为 主产品编码-001。
        4. Product code must be Unique.产品编码强制要求唯一。
        5. Quick default value for every category. 按指定目录生成指定产品默认值，。
        6. Multi language support.多语种支持。
    """,
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'depends': [
        'product',
        'stock',
        # 'sale',
        # 'purchase',
        # 'mrp',
                ],
    'data': [
        # 视图
        'views/product_category_views.xml',
        'views/product_template_view.xml',
        'data/product_sequence.xml',
        'data/product_data.xml',
    ],
    'demo': [
    ],
}
