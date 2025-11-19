import frappe

def execute():
    # Only create if it doesn't exist
    if not frappe.db.exists("Custom Field", "Stock Entry-work_plan"):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Stock Entry",
            "fieldname": "work_plan",
            "label": "Work Plan",
            "fieldtype": "Link",
            "options": "Work Plan",
            "insert_after": "purchase_receipt_no"
        }).insert()
        frappe.db.commit()
        print("Successfully Added")
    else:
        print("Already Added")
