from odoo import models, api

class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    @api.model
    def _get_component_data(self, parent_bom, parent_product, warehouse, bom_line, line_quantity, level, index, product_info, ignore_stock=False):
        res = super()._get_component_data(parent_bom, parent_product, warehouse, bom_line, line_quantity, level, index, product_info, ignore_stock=False)
        res['secondary_qty'] = bom_line.secondary_qty
        res['secondary_uom'] = bom_line.secondary_uom_id.name
        return res
