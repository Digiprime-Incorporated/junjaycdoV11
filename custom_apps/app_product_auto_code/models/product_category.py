# -*- coding: utf-8 -*-

# Created on 2017-11-28
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

from odoo import api, fields, models, exceptions, _

class ProductCategory(models.Model):
    _inherit = 'product.category'
    _order = 'sequence, ref'

    active = fields.Boolean(default=True, help="Set active to false to hide the item without removing it.")
    ref = fields.Char(u'Unique Code', index=True)
    sequence = fields.Integer(u'Sequence', help="Determine the display order")
    type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ('product', 'Stockable Product')], string='Default Product Type',
        help='Product in this category would set default type to this value.')

    sale_ok = fields.Boolean(
        'Default Can be Sold', default=True,
        help="Specify if the product can be selected in a sales order line.")
    purchase_ok = fields.Boolean('Default Can be Purchased', default=True)
    rental = fields.Boolean('Default Can be Rent')

    product_sequence = fields.Many2one(
        'ir.sequence', 'Product Sequence',
        auto_join=True, domain="[('code', 'ilike', 'product.product')]")
    sequence_prefix = fields.Char(u'Sequence Prefix', related='product_sequence.prefix', readonly=True, store=False)

    # 增加目录编号唯一检查
    _sql_constraints = [
        ('uniq_ref',
         'unique(ref)',
         'The reference must be unique'),
    ]

    # 产品目录序号器，产生默认值，或者手工录入
    @api.model
    def default_get(self, fields):
        res = super(ProductCategory, self).default_get(fields)
        if 'ref' in res and res.ref != _('New'):
            pass
        else:
            try:
                res.update({'ref': self.env['ir.sequence'].next_by_code('product.category.default')})
            except Exception as e:
                pass
        return res


    # @api.model
    # def create(self, vals):
    #     if 'ref' not in vals or vals['ref'] == _('New'):
    #         vals['ref'] = self.env['ir.sequence'].next_by_code('product.category.default')
    #     if vals.get('ref'):
    #         vals['ref'] = vals['ref'].upper()
    #     return super(ProductCategory, self).create(vals)

