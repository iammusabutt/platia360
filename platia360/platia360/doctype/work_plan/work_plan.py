# Copyright (c) 2025, Platia360 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate


class WorkPlan(Document):
	pass

@frappe.whitelist()
def fetch_ppm_items_from_template(template_name):
    """
    Fetch child table items from PPM Checklist Template
    """
    if not template_name:
        return []

    template = frappe.get_doc("PPM Checklist Template", template_name)

    ppm_items_list = []
    for item in template.get("ppm_items"):
        ppm_items_list.append({
            "ppm_item_sequence": item.ppm_item_sequence,
            "ppm_item_task": item.ppm_item_task,
            "ppm_item_must": item.ppm_item_must,
            "ppm_item_done": item.ppm_item_done,
            "ppm_item_expected_result": item.ppm_item_expected_result,
            "ppm_item_date": item.ppm_item_date,
            "ppm_item_owner": item.ppm_item_owner,
            "ppm_item_skills": item.ppm_item_skills,
            "ppm_item_status": item.ppm_item_status,
            "ppm_item_remarks": item.ppm_item_remarks,
        })

    return ppm_items_list


@frappe.whitelist()
def make_stock_entry(work_plan, target_doc=None):
    wp = frappe.get_doc("Work Plan", work_plan)

    se = frappe.new_doc("Stock Entry")
    se.stock_entry_type = "Material Transfer"
    se.custom_work_plan = wp.name  # custom field
    
    if wp.required_items:
        for row in wp.required_items:
            se.append("items", {
                "item_code": row.item_code,
                "qty": row.required_qty,
                "uom": row.stock_uom,
                "stock_uom": row.stock_uom,
                "conversion_factor": 1,
                "s_warehouse": row.source_warehouse,
                "t_warehouse": row.source_warehouse,
                "rate": row.rate,
            })

    return se

