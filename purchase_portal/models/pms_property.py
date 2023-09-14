##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2023 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#    Vicente Ángel Gutiérrez <vicente@comunitea.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import fields, models, api, _
from odoo.exceptions import AccessDenied


class PMSProperty(models.Model):
    _inherit = 'pms.property'
    
    product_ids = fields.Many2many(
        'product.product',
        string='Allowed products',
        relation="pms_property_product_product_rel",
        column1="product_id",
        column2="property_id",
    )
    seller_id = fields.Many2one(
        'res.partner', 'Vendor',
        help="Vendor allowed in this property."
    )
    wharehouse_id = fields.Many2one('stock.warehouse', 'Warehouse')

    @api.onchange("seller_id")
    def onchange_seller_id(self):
        if self.seller_id:
            seller_products = self.env['product.supplierinfo'].search([('name', '=', self.seller_id.id)])
            seller_product_product = seller_products.mapped('product_tmpl_id.product_variant_ids')
            seller_product_product += seller_products.mapped('product_id')
            self.product_ids = seller_product_product.ids
