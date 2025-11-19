from frappe import _

def get_data():
    return {
        "fieldname": "work_plan",   # Link field in other Doctypes
        "non_standard_fieldnames": {
            # If the linked doctype uses a different fieldname, define here
            # Example:
            # "Stock Entry": "custom_work_plan_link"
        },
        "transactions": [
            {
                "items": ["Stock Entry"]   # Any doctype you want to show
            }
        ],
    }
