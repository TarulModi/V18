from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import csv
import openpyxl
from io import BytesIO

class BomImport(models.TransientModel):
    _name = 'bom.import'
    _description = 'Import BOM Wizard'

    file = fields.Binary('File')
    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select', default='csv')
    import_product_by = fields.Selection([('name', 'Name'),('code', 'Code'),('barcode', 'Barcode')], string='Import Product By', default='name')

    def action_import_bom(self):
        if not self.file:
            raise UserError(_('Please Upload a File to proceed.'))
        if self.import_option == 'csv':
            self._import_bom_csv()
        elif self.import_option == 'xls':
            self._import_bom_xls()

    def _import_bom_csv(self):
        try:
            file = base64.b64decode(self.file).decode('utf-8')
            reader = csv.reader(file.splitlines())
            next(reader)  # Skip the header
            rec_count = 0
            last_bom_id = False

            for col in reader:
                if col:
                    # # Validate if the necessary columns are present
                    # if len(col) < 8:
                    #     raise UserError(_('Missing required data in CSV row: %s') % str(col))
                    #
                    # if not col[0]:
                    #     raise UserError(_('Missing product name in CSV row: %s') % str(col))
                    # if not col[3]:
                    #     raise UserError(_('Missing product quantity in CSV row: %s') % str(col))
                    # if not col[4]:
                    #     raise UserError(_('Missing unit of measure in CSV row: %s') % str(col))

                    # BOM Type validation (check if subcontract is selected but no subcontractor is provided)
                    bom_type = col[5].strip().lower() if len(col) > 5 and col[5] else 'normal'
                    if bom_type == 'subcontract' and not col[6]:
                        raise UserError(_('Missing subcontractor in CSV row: %s') % str(col))

                    if self.import_product_by == 'name':
                        product = self._search_product(col[0])
                    elif self.import_product_by == 'code':
                        product = self._search_product(col[2])
                    elif self.import_product_by == 'barcode':
                        product = self._search_product(col[2])
                    else:
                        product = self._search_product(col[0])

                    variant = self._search_variant(col[1]) if col[1] else None
                    if not variant:
                        variant = self.env['product.product'].search([('product_tmpl_id', '=', product.id)], limit=1)

                    if bom_type not in ['normal', 'phantom', 'subcontract']:
                        bom_type = 'normal'

                    subcontractor_ids = col[6] if len(col) > 6 and col[6] else False
                    if subcontractor_ids:
                        subcontractor = self.env['res.partner'].search([('name', '=', subcontractor_ids)], limit=1)
                        subcontractor_ids = [(6, 0, [subcontractor.id])] if subcontractor else False

                    code = col[7] if len(col) > 7 and col[7] else False

                    bom_data = {
                        'product_tmpl_id': product.product_tmpl_id.id,
                        'product_id': product.id if product else False,
                        'product_qty': float(col[3]) if len(col) > 3 and col[3] else 1.0,
                        'type': bom_type,
                        'subcontractor_ids': subcontractor_ids,
                        'code': code,
                    }

                    if col[4]:
                        uom = self.env['uom.uom'].search([('name', '=', col[4])], limit=1)
                        bom_data.update({'product_uom_id': uom.id})

                    bom_bom = self.env['mrp.bom'].create(bom_data)
                    last_bom_id = bom_bom.id

                if len(col) > 8 and col[8]:
                    # Validate if the component data is correct
                    if not col[8]:
                        raise UserError(_('Missing component in CSV row: %s') % str(col))
                    if not col[9]:
                        raise UserError(_('Missing component quantity in CSV row: %s') % str(col))

                    if not self.import_product_by == 'name':
                        component_variant = self._search_product(col[11])
                    else:
                        component_variant = self._search_variant(col[8])
                    component_qty = float(col[9]) if len(col) > 9 and col[9] else 1.0
                    component_uom = col[10] if len(col) > 10 and col[10] else None

                    bom_line_data = {
                        'product_id': component_variant.id,
                        'bom_id': last_bom_id,
                        'product_qty': component_qty,
                        'product_uom_id': component_variant.uom_id.id if component_uom else False,
                    }
                    self.env['mrp.bom.line'].create(bom_line_data)

            return
        except Exception as e:
            raise UserError(_('Error processing CSV file: %s') % str(e))

    def _import_bom_xls(self):
        try:
            wb = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(self.file)), read_only=True)
            ws = wb.active
            rec_count = 0
            last_bom_id = False
            last_name = None

            for col in ws.iter_rows(min_row=2, values_only=True):
                if col:
                    product = False

                    # Validate if the necessary columns are present
                    # if len(col) < 8:
                    #     raise UserError(_('Missing required data in XLS row: %s') % str(col))
                    #
                    # if not col[0]:
                    #     raise UserError(_('Missing product name in XLS row: %s') % str(col))
                    # if not col[3]:
                    #     raise UserError(_('Missing product quantity in XLS row: %s') % str(col))
                    # if not col[4]:
                    #     raise UserError(_('Missing unit of measure in XLS row: %s') % str(col))

                    # if col[5] and (col[5] != 'Manufacture this product') or :
                    #     raise UserError(_("BOM type '%s' not found") % col[5])

                    # BOM Type validation (check if subcontract is selected but no subcontractor is provided)
                    bom_type = col[5].strip().lower() if len(col) > 5 and col[5] else 'normal'
                    if bom_type == 'subcontract' and not col[6]:
                        raise UserError(_('Missing subcontractor in XLS row: %s') % str(col))

                    # if self.import_product_by == 'name':
                    #     product = self._search_product(col[0])
                    # if self.import_product_by == 'code':
                    #     product = self._search_product(col[2])
                    if self.import_product_by == 'barcode' or self.import_product_by == 'code':
                        if col[2]:
                            product = self._search_product(col[2])
                        else:
                            if not col[2] and col[5]:
                                if self.import_product_by == 'barcode':
                                    raise UserError(_("Product barcode is required.!"))
                                else:
                                    raise UserError(_("Product code is required.!"))
                    else:
                        if col[0]:
                            product = self._search_product(col[0])
                        else:
                            if not col[0] and col[5]:
                                raise UserError(_("Product name is required.!"))
                    # if self.import_product_by == 'name':
                    #     print("-------d------",col)
                    #     print("-------------",col[0])
                    #     print("-------last_name------",last_name)
                    #     if not col[0] and not last_name:
                    #         raise UserError(_("Product name is required.!"))
                    #     if col[0]:
                    #         product = self._search_product(col[0])
                    #         last_name = product
                    #         print("---last_name----------",last_name)
                    # elif self.import_product_by == 'code':
                    #     if not col[2] and not last_name:
                    #         raise UserError(_("Product code is required.!"))
                    #     if col[2]:
                    #         product = self._search_product(col[2])
                    #         last_name = product
                    # elif self.import_product_by == 'barcode':
                    #     if not col[2] and not last_name:
                    #         raise UserError(_("Product barcode is required.!"))
                    #     if col[2]:
                    #         product = self._search_product(col[2])
                    #         last_name = product
                    # else:
                    #     if not col[0] and not last_name:
                    #         raise UserError(_("Product name is required.!"))
                    #     if col[0]:
                    #         product = self._search_product(col[0])
                    #         last_name = product

                    # variant = self._search_variant(col[1]) if col[1] else None
                    # if not variant:
                    #     variant = self.env['product.product'].search([('product_tmpl_id', '=', product.id)], limit=1)

                    if bom_type not in ['kit', 'manufacture this product', 'subcontract', 'normal']:
                        raise UserError(_('BOM type "%s" not found.') % (bom_type))

                    if bom_type not in ['normal', 'kit', 'subcontract']:
                        bom_type = 'normal'

                    if bom_type == 'kit':
                        bom_type = 'phantom'

                    # subcontractor_ids = col[6] if len(col) > 6 and col[6] else False
                    # print("----subcontractor_ids---------------",subcontractor_ids)
                    # if subcontractor_ids:
                    #     print("----subcontractor_ids-------22222--------",subcontractor_ids)
                    #     subcontractor = self.env['res.partner'].search([('name', '=', subcontractor_ids)], limit=1)
                    #     print("----subcontractor-------22222--------",subcontractor)
                    #     subcontractor_ids = [(6, 0, [subcontractor.id])] if subcontractor else False

                    subcontractor_ids = col[6] if len(col) > 6 and col[6] else False
                    if subcontractor_ids:
                        subcontractor_names = [name.strip() for name in subcontractor_ids.split(',')]
                        subcontractors = self.env['res.partner'].search([('name', 'in', subcontractor_names)])
                        found_names = subcontractors.mapped('name')
                        missing_names = set(subcontractor_names) - set(found_names)
                        if missing_names:
                            raise UserError(
                                f"The following subcontractors do not exist in the system: {', '.join(missing_names)}")
                        subcontractor_ids = [(6, 0, subcontractors.ids)]

                    code = col[7] if len(col) > 7 and col[7] else False

                    print("-----product----333333333333333-----",product)
                    if product and product.product_tmpl_id:
                        bom_data = {
                            'product_tmpl_id': product.product_tmpl_id.id,
                            'product_id': product.id if product else False,
                            'product_qty': float(col[3]) if len(col) > 3 and col[3] else 1.0,
                            'type': bom_type,
                            'subcontractor_ids': subcontractor_ids,
                            'code': code,
                        }
                        if col[4]:
                            uom = self.env['uom.uom'].search([('name', '=', col[4])], limit=1)
                            if not uom:
                                raise UserError(_('UOM "%s" is not found') % str(col[4]))
                            bom_data.update({'product_uom_id': uom.id})

                        bom_bom = self.env['mrp.bom'].create(bom_data)
                        last_bom_id = bom_bom.id
                        print("-----last_bom_id---------", last_bom_id)

                if len(col) > 8:
                    component_variant = False

                    # if col and col[8]:
                    if not self.import_product_by == 'name':
                        component_variant = self._search_product(col[11])
                        if not col[11]:
                            if self.import_product_by == 'code':
                                raise UserError(_("Component code is required.!"))
                            else:
                                raise UserError(_("Component barcode is required.!"))
                    else:
                        if not col[8]:
                            raise UserError(_("Component name is required.!"))
                        component_variant = self._search_product(col[8])
                    # else:
                    #     component_variant = False
                    component_qty = float(col[9]) if len(col) > 9 and col[9] else 1.0
                    # component_uom = col[10] if len(col) > 10 and col[10] else None
                    uom = False
                    if col[10]:
                        uom = self.env['uom.uom'].search([('name', '=', col[10])], limit=1)
                        if not uom:
                            raise UserError(_('UOM "%s" is not found') % str(col[10]))

                    if uom:
                        uom_id = uom.id
                    else:
                        uom_id = component_variant.uom_id.id

                    print("----------component_variant-----", component_variant)
                    print("----------last_bom_id-----", last_bom_id)
                    if component_variant:
                        bom_line_data = {
                            'product_id': component_variant.id,
                            'bom_id': last_bom_id,
                            'product_qty': component_qty,
                            'product_uom_id': uom_id,
                        }
                        self.env['mrp.bom.line'].create(bom_line_data)

            return
        except Exception as e:
            raise UserError(_('Error processing XLS file: %s') % str(e))

    def _search_product(self, value):
        print("======value========",value)
        if self.import_product_by == 'code':
            domain = [('default_code', '=', value)]
        elif self.import_product_by == 'barcode':
            domain = [('barcode', '=', value)]
        elif self.import_product_by == 'name':
            domain = [('name', '=', value)]
        else:
            domain = [('name', '=', value)]

        product = self.env['product.product'].search(domain, limit=1)
        print("======product========",product)
        if not product:
            raise UserError(_('Product with %s "%s" not found.') % (self.import_product_by, value))
        return product

    def _search_variant(self, value):
        domain = [(self.import_product_by, '=', value)]
        return self.env['product.product'].search(domain, limit=1)
