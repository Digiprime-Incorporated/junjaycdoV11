# -*- coding: utf-8 -*-

# Created on 2018-11-01
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
from odoo import models, fields, api, exceptions, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char('Internal Reference', index=True, default=lambda self: _('New'), copy=False)
    default_code_index = fields.Integer('Internal Reference Index', readonly=True)

    # todo: 检查数据，要保证数据唯一性
    _sql_constraints = [
        ('uniq_default_code',
         'unique(default_code)',
         'The reference must be unique. Try save again.'),
    ]

    @api.model
    def default_get(self, fields):
        context = self._context or {}
        res = super(ProductProduct, self).default_get(fields)
        # 内部编码类型默认值的录入
        if 'categ_id' in res:
            self._onchange_categ_id()
        return res

    @api.model
    def create(self, vals):
        # todo: but 先建空白产品后，编辑2个以上变体，序号会少个 -1
        # code_index: 当没有变体现时，值为0，有变体时，为该变体序号
        code_index = 0
        if 'default_code' not in vals or vals['default_code'] == _('New'):
            if 'product_tmpl_id' in vals:
                # 按产品模板创建产品，有多种情况
                template = self.env['product.template'].search([('id', '=', vals['product_tmpl_id'])], limit=1)
                if template.default_code and template.default_code != '':
                    code_stored = template.default_code
                else:
                    code_stored = template.default_code_stored
                if not code_stored:
                    code_stored = ''
                mylen = len(template.product_variant_ids)
                try:
                    attr = vals['attribute_value_ids'][0][2]
                except:
                    attr = 0

                # if self.env.context.get('create_from_tmpl') and not(attr): 此条件已限制，不让在template中先直接创建变体，要求先保存
                if self.env.context.get('create_from_tmpl') and not (attr):
                    # 从产品模板创建的第一个sku产品，不带属性
                    # 没有属性值，则是单规格产品。attribute_value_ids格式为[6,0,[]]。多规格时，attribute_value_ids格式为[6,0,[x]]
                    code_index = 0
                    vals['default_code_index'] = code_index
                    vals['default_code'] = code_stored
                elif mylen == 0:
                    # 有属性值了，自己是第一个规格
                    code_index = 1
                    vals['default_code_index'] = code_index
                    vals['default_code'] = code_stored + '#%03d' % (code_index)
                elif mylen == 1:
                    # 已存在1个，当存在的1个有属性时，要改已存在的product值
                    code_index = template.product_variant_ids[:1].default_code_index
                    if template.product_variant_ids[:1].attribute_value_ids:
                        if code_index == 0:
                            code_index = 1
                        template.product_variant_ids[:1].default_code_index = code_index
                        template.product_variant_ids[:1].default_code = code_stored + '#%03d' % (code_index)
                    # 接着改当前操作的product值
                    code_index = code_index + 1
                    vals['default_code_index'] = code_index
                    vals['default_code'] = code_stored + '#%03d' % (code_index)
                elif mylen > 1:
                    # 找到最大的序号
                    variant_max = max(template.product_variant_ids, key=lambda x: x['default_code_index'])
                    code_index = variant_max['default_code_index'] + 1
                    vals['default_code_index'] = code_index
                    vals['default_code'] = code_stored + '#%03d' % (code_index)
                else:
                    # 当按模板
                    # 此条件常规不出现，但特殊项目会有
                    variant_max = max(template.product_variant_ids, key=lambda x: x['default_code_index'])
                    code_index = variant_max['default_code_index'] + 1
                    vals['default_code_index'] = code_index
                    vals['default_code'] = code_stored + '#%03d' % (code_index)
            else:
                # create from product_product
                # 默认使用普通品的编码
                sequence = self.env.ref('app_product_auto_code.seq_product_default', raise_if_not_found=False)
                if 'categ_id' in vals:
                    cat = self.env['product.category'].search([('id', '=', vals['categ_id'])], limit=1)
                    if cat and cat.product_sequence:
                        sequence = cat.product_sequence
                vals['default_code'] = sequence.next_by_id()
        else:
            # 如果有自己输入 ref，则不需要自动生成
            pass
        return super(ProductProduct, self).create(vals)

    @api.multi
    def copy(self, default=None):
        if len(self.product_tmpl_id.product_variant_ids) > 1:
            raise exceptions.ValidationError(_('Product varient can only create in Product view!'))
        return super(ProductProduct, self).copy(default=None)

    # 当产品目录变化时，改变产品的各默认值
    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        if self.categ_id:
            self.type = self.categ_id.type
            self.rental = self.categ_id.rental
            self.sale_ok = self.categ_id.sale_ok
            self.purchase_ok = self.categ_id.purchase_ok
