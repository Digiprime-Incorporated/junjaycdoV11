# -*- coding: utf-8 -*-

from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    sticky_th_shadow = fields.Boolean("Shadow while floating")
    sticky_th_noborder = fields.Boolean("Reduce borders")
    sticky_th_always = fields.Boolean("Reduce ListView's Flicker")
    sticky_th_alwaysshadow = fields.Boolean("Shadow")
    sticky_th_pivot = fields.Boolean("Pivot Header Sticky")


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        xml_o = self.env['ir.model.data'].sudo().xmlid_to_object
        res.update(
            sticky_th_shadow=xml_o('sticky_th.sticky_th_shadow', True).active,
            sticky_th_noborder=xml_o('sticky_th.sticky_th_noborderbottom', True).active,
            sticky_th_always=xml_o('sticky_th.sticky_th_always', True).active,
            sticky_th_alwaysshadow=xml_o('sticky_th.sticky_th_always2', True).active,
            sticky_th_pivot=xml_o('sticky_th.pivot_assets_backend', True).active,
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        xml_o = self.env['ir.model.data'].sudo().xmlid_to_object
        xml_o('sticky_th.sticky_th_shadow', True).active = self.sticky_th_shadow
        xml_o('sticky_th.sticky_th_noborderbottom', True).active = self.sticky_th_noborder
        xml_o('sticky_th.sticky_th_always', True).active = self.sticky_th_always
        xml_o('sticky_th.sticky_th_always2', True).active = self.sticky_th_alwaysshadow
        xml_o('sticky_th.pivot_assets_backend', True).active = self.sticky_th_pivot
        

