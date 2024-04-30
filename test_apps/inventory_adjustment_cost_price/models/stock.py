# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockInventoryLine(models.Model):
    """Extend to add cost field."""

    _inherit = 'stock.inventory.line'

    unit_cost = fields.Monetary("Unit Cost")
    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        default=lambda self: self.company_id.currency_id
    )

    @api.multi
    def _get_move_values(self, qty, location_id, location_dest_id, out):
        """
        Extend to add unit cost.

        Args:
            qty (float): Product quantity.
            location_id (int): Source location id.
            location_dest_id (int): Destination lacation id.
            out (bool): Out

        Returns:
            (dict): Values for stock move.
        """
        self.ensure_one()
        res = super(StockInventoryLine, self)._get_move_values(
            qty, location_id, location_dest_id, out
        )
        if self.unit_cost:
            res['price_unit'] = self.unit_cost
        return res
