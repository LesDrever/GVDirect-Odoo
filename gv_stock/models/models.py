# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class GVDescription(models.Model):
    _name = 'gv.description'
    _description = "GV Description"

    name = fields.Char(string="Name", required=True)


class GVProductTemplate(models.Model):
    _inherit = 'product.template'

    description_internal_transfer_ids = fields.Many2many('gv.description', string='Description for Internal Transfers')


class GVStockMove(models.Model):
    _inherit = "stock.move"

    description_internal_transfer_ids = fields.Many2many(related="product_id.description_internal_transfer_ids", string='Picking Description')

    @api.onchange('description_internal_transfer_ids')
    def _onchange_description_internal_transfer_ids(self):
        if not self.product_id:
            return
        self.product_id.update({'description_internal_transfer_ids': self.description_internal_transfer_ids.ids})
        return {'warning': {
            'title': _("Warning for %s") % self.product_id.name,
            'message': _("Changing Picking Description also changes in product.")
        }}


class GVStockMoveLine(models.Model):
    _inherit = "stock.move.line"

    description_internal_transfer_ids = fields.Many2many(related="product_id.description_internal_transfer_ids", string='Picking Description')

    @api.onchange('description_internal_transfer_ids')
    def _onchange_description_internal_transfer_ids(self):
        if not self.product_id:
            return
        self.product_id.update({'description_internal_transfer_ids': self.description_internal_transfer_ids.ids})
        return {'warning': {
            'title': _("Warning for %s") % self.product_id.name,
            'message': _("Changing Picking Description also changes in product.")
        }}
