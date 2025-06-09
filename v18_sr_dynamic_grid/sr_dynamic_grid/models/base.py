from odoo import api, fields, models, tools, _
from lxml import etree
from odoo.tools import config, lazy_property, frozendict, SQL


class Model(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        result = super().get_view(view_id, view_type, **options)

        if view_type == 'list' and result['id']:
            user_layout_id = self.env['user.layout'].search([
                ('user_id','=',self.env.user.id),
                ('layout_id.view_id','=',result['id']),
                ('is_selected','=',True)
            ],limit=1)
            if user_layout_id:
                field_list = user_layout_id.layout_id.layout
                if field_list:
                    field_list = field_list.split(',')
                    field_dict = dict()
                    node = etree.fromstring(result['arch'])
                    for field in [elem for elem in node.findall('.//field') if 'position' not in elem.attrib]:
                        if field.get('name') in field_list:
                            field_dict[field.get('name')] = field.attrib
                        field.set('column_invisible', '1')
                    node = etree.tostring(node)
                    node = etree.fromstring(node)
                    tree = etree.ElementTree(node)
                    target = tree.getroot()
                    for field in field_list:
                        f = etree.Element('field')
                        f.set("name", field)
                        if field in field_dict:
                            for attribute,value in field_dict[field].items():
                                if attribute not in ['optional','column_invisible','name']:
                                    f.set(attribute, value)
                        target.append(f)
                    node = etree.tostring(node)
                    result['arch'] = node
        return result