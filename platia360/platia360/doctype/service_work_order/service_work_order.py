# Copyright (c) 2025, Platia360 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ServiceWorkOrder(Document):
	pass

@frappe.whitelist()
def make_work_plan(source_name, target_doc=None):
    wp_source = frappe.get_doc("Service Work Order", source_name)

    wp_target = frappe.new_doc("Work Plan")

    # Map your fields here
    wp_target.jobwo = wp_source.name


    # return doc — do not insert yet
    return wp_target
