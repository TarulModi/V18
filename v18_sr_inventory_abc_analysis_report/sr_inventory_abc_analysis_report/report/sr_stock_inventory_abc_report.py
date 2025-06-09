# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import api, models, _
from operator import itemgetter

#Report Inventory ABC Analysis Report Template Class.
class srInventoryAbcAnalysisReport(models.AbstractModel):
    _name = "report.sr_inventory_abc_analysis_report.abc_template"
    _description = "Inventory ABC Analyse Report Template"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["stock.inventory.abc.report"].browse(docids)
        product_dict_list = []
        sorted_sold_uint_list = []
        sorted_consumption_list = []
        category_list = []
        category_dict_list = []
        total_sold_units = 0.0
        total_consumption_value = 0.0

        sale_order_ids = self.env["sale.order"].search(
            [
                ("date_order", ">=", docs.from_date),
                ("date_order", "<=", docs.to_date),
                ("state", "in", ["done", "sale"]),
            ]
        )
        if sale_order_ids:
            product_groups = sale_order_ids.order_line.read_group(
                domain=[("order_id", "in", sale_order_ids.ids)],
                fields=["product_id", "product_uom_qty"],
                groupby=["product_id", "product_uom_qty"],
            )
            for product_group in product_groups:
                product_obj = self.env["product.product"].browse(
                    product_group["product_id"][0]
                )
                if docs.abc_base_on == "product_categ":
                    product_cat_groups = product_obj.read_group(
                        domain=[("id", "in", product_obj.ids)],
                        fields=["categ_id"],
                        groupby=["categ_id"],
                    )
                    if product_cat_groups:
                        for product_cat_grp in product_cat_groups:
                            product_cat_obj = self.env["product.category"].browse(
                                product_cat_grp["categ_id"][0]
                            )
                            product_dict_list.append(
                                {
                                    "product": product_obj.name,
                                    "category_name": product_cat_obj.name,
                                    "product_qty": product_group["product_uom_qty"],
                                    "product_cost": product_obj.standard_price,
                                }
                            )
                else:
                    product_dict_list.append(
                        {
                            "product": product_obj.name,
                            "product_qty": product_group["product_uom_qty"],
                            "product_cost": product_obj.standard_price,
                        }
                    )
            if product_dict_list and docs.abc_base_on == "products":
                consumption_value = 0.0
                for product_dict in product_dict_list:
                    total_sold_units += product_dict["product_qty"]
                    consumption_value = (
                        product_dict["product_cost"] * product_dict["product_qty"]
                    )
                    product_dict["consumption_value"] = consumption_value
                    total_consumption_value += consumption_value
                    product_dict["total_consumption_value"] = total_consumption_value
                per_sold_unit_cal = 0.0
                per_consumption_value_cal = 0.0
                per_of_consumption_value = 0.0
                value_for_a = True
                value_for_b = True
                fill_value_for_a = True
                if total_sold_units and docs.classification_by == "sold_unit":
                    sorted_sold_uint_list = sorted(
                        product_dict_list, key=itemgetter("product_qty"), reverse=True
                    )
                    for product_dict_lst in sorted_sold_uint_list:
                        per_of_sold_unit = (
                            product_dict_lst["product_qty"] / total_sold_units
                        ) * 100
                        product_dict_lst["per_of_sold_unit"] = per_of_sold_unit
                        per_sold_unit_cal += per_of_sold_unit
                        if per_sold_unit_cal < 80.0 and value_for_a:
                            product_dict_lst["classification"] = "A"
                            fill_value_for_a = False
                        else:
                            if ("classification" not in product_dict_lst and fill_value_for_a):
                                product_dict_lst["classification"] = "A"
                                value_for_a = False
                                fill_value_for_a = False
                                per_sold_unit_cal = per_of_sold_unit
                            else:
                                value_for_a = False
                                if value_for_b:
                                    per_sold_unit_cal = per_of_sold_unit
                                if per_sold_unit_cal < 15.0:
                                    product_dict_lst["classification"] = "B"
                                    value_for_b = False
                                else:
                                    if value_for_b:
                                        product_dict_lst["classification"] = "B"
                                        value_for_b = False
                                    else:
                                        product_dict_lst["classification"] = "C"
                else:
                    if total_consumption_value:
                        sorted_consumption_list = sorted(
                            product_dict_list,
                            key=itemgetter("consumption_value"),
                            reverse=True,
                        )
                        for product_dict_lst in sorted_consumption_list:
                            per_of_consumption_value = (
                                product_dict_lst["consumption_value"]
                                / total_consumption_value
                            ) * 100
                            product_dict_lst[
                                "per_of_consumption_value"
                            ] = per_of_consumption_value
                            per_consumption_value_cal += per_of_consumption_value
                            if per_consumption_value_cal < 80.0 and value_for_a:
                                product_dict_lst["classification"] = "A"
                                fill_value_for_a = False
                            else:
                                if "classification" not in product_dict_lst and fill_value_for_a:
                                    product_dict_lst["classification"] = "A"
                                    value_for_a = False
                                    fill_value_for_a = False
                                    per_consumption_value_cal = per_of_consumption_value
                                else:
                                    value_for_a = False
                                    if value_for_b:
                                        per_consumption_value_cal = per_of_consumption_value
                                    if per_consumption_value_cal < 15.0:
                                        product_dict_lst["classification"] = "B"
                                        value_for_b = False
                                    else:
                                        if value_for_b:
                                            product_dict_lst["classification"] = "B"
                                            value_for_b = False
                                        else:
                                            product_dict_lst["classification"] = "C"
            else:
                sorted_list = sorted(product_dict_list, key=itemgetter("category_name"))
                category_sold_units = 0.0
                for sort_lst in sorted_list:
                    if category_dict_list:

                        for category_dic in category_dict_list:
                            if sort_lst["category_name"] == category_dic.get(
                                "category_name"
                            ):
                                category_dic["category_sold_units"] += sort_lst[
                                    "product_qty"
                                ]
                                category_dic["category_consumption_value"] += (
                                    sort_lst["product_qty"] * sort_lst["product_cost"]
                                )
                            else:
                                category_sold_units = 0.0
                                if sort_lst["category_name"] not in category_list:
                                    category_dict_list.append(
                                        {
                                            "category_name": sort_lst["category_name"],
                                            "category_sold_units": sort_lst[
                                                "product_qty"
                                            ],
                                            "category_consumption_value": sort_lst[
                                                "product_qty"
                                            ]
                                            * sort_lst["product_cost"],
                                        }
                                    )
                                    category_list.append(sort_lst["category_name"])
                                    break
                    else:
                        category_dict_list.append(
                            {
                                "category_name": sort_lst["category_name"],
                                "category_sold_units": sort_lst["product_qty"],
                                "category_consumption_value": sort_lst["product_qty"]
                                * sort_lst["product_cost"],
                            }
                        )
                        category_list.append(sort_lst["category_name"])
                if category_dict_list:
                    for cat_lst in category_dict_list:
                        total_sold_units += cat_lst["category_sold_units"]
                        total_consumption_value += cat_lst["category_consumption_value"]
                    per_sold_unit_cal = 0.0
                    per_consumption_value_cal = 0.0
                    per_of_consumption_value = 0.0
                    value_for_a = True
                    value_for_b = True
                    fill_value_for_a = True
                    if total_sold_units and docs.classification_by == "sold_unit":
                        sorted_sold_uint_list = sorted(
                            category_dict_list,
                            key=itemgetter("category_sold_units"),
                            reverse=True,
                        )
                        for product_dict_lst in sorted_sold_uint_list:
                            per_of_sold_unit = (
                                product_dict_lst["category_sold_units"]
                                / total_sold_units
                            ) * 100
                            product_dict_lst["per_of_sold_unit"] = per_of_sold_unit
                            per_sold_unit_cal += per_of_sold_unit
                            if per_sold_unit_cal < 80.0 and value_for_a:
                                product_dict_lst["classification"] = "A"
                                fill_value_for_a = False
                            else:
                                if ("classification" not in product_dict_lst and fill_value_for_a):
                                    product_dict_lst["classification"] = "A"
                                    value_for_a = False
                                    fill_value_for_a = False
                                    per_sold_unit_cal = (per_of_sold_unit)
                                else:
                                    value_for_a = False
                                    if value_for_b:
                                        per_sold_unit_cal = (per_of_sold_unit)
                                    if per_sold_unit_cal < 15.0:
                                        product_dict_lst["classification"] = "B"
                                        value_for_b = False
                                    else:
                                        if value_for_b:
                                            product_dict_lst["classification"] = "B"
                                            value_for_b = False
                                        else:
                                            product_dict_lst["classification"] = "C"
                    else:
                        if total_consumption_value:
                            sorted_consumption_list = sorted(
                                category_dict_list,
                                key=itemgetter("category_consumption_value"),
                                reverse=True,
                            )
                            for product_dict_lst in sorted_consumption_list:
                                per_of_consumption_value = (
                                    product_dict_lst["category_consumption_value"]
                                    / total_consumption_value
                                ) * 100
                                product_dict_lst[
                                    "per_of_consumption_value"
                                ] = per_of_consumption_value
                                per_consumption_value_cal += per_of_consumption_value
                                if per_consumption_value_cal < 80.0 and value_for_a:
                                    product_dict_lst["classification"] = "A"
                                    fill_value_for_a = False
                                else:
                                    if (
                                        "classification" not in product_dict_lst
                                        and fill_value_for_a
                                    ):
                                        product_dict_lst["classification"] = "A"
                                        value_for_a = False
                                        fill_value_for_a = False
                                        per_consumption_value_cal = (
                                            per_of_consumption_value
                                        )
                                    else:
                                        value_for_a = False
                                        if value_for_b:
                                            per_consumption_value_cal = (
                                                per_of_consumption_value
                                            )
                                        if per_consumption_value_cal < 15.0:
                                            product_dict_lst["classification"] = "B"
                                            value_for_b = False
                                        else:
                                            if value_for_b:
                                                product_dict_lst["classification"] = "B"
                                                value_for_b = False
                                            else:
                                                product_dict_lst["classification"] = "C"
        if sorted_sold_uint_list:
            sorted_product_dict_list = sorted_sold_uint_list
        else:
            sorted_product_dict_list = sorted_consumption_list
        return {
            "docs": docs,
            "items_data": sorted_product_dict_list,
            "total_consumption_value": total_consumption_value,
            "total_sold_units": total_sold_units,
        }
