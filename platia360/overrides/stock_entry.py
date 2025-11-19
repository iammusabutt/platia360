import frappe

def link_to_work_plan(doc, method)
    # Debug: show doc values in UI
    frappe.msgprint(f"Debug Stock Entry.name: {doc.name}")
    frappe.msgprint(f"Debug Stock Entry.custom_work_plan: {doc.custom_work_plan}")

    if doc.custom_work_plan:
        work_plan_name = doc.custom_work_plan
        stock_entry_name = doc.name

        # Check if Work Plan exists
        if frappe.db.exists("Work Plan", work_plan_name):
            # Optional: only update if stock_entry is empty
            current_value = frappe.db.get_value("Work Plan", work_plan_name, "stock_entry")
            if not current_value:
                frappe.db.set_value("Work Plan", work_plan_name, "stock_entry", stock_entry_name)
                frappe.db.commit()
                frappe.msgprint(f"Work Plan {work_plan_name} updated with Stock Entry {stock_entry_name}")
        else:
            frappe.log_error(f"Work Plan {work_plan_name} not found", "Stock Entry linking failed")
