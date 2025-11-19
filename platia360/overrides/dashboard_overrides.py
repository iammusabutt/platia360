# Copyright (c) 2025, Platia360
# License: GNU General Public License v3

from frappe import _

def get_dashboard_for_work_plan(data):

    # Optional: map non-standard fieldnames if needed
    data["non_standard_fieldnames"].update({
        "Stock Entry": "custom_work_plan"  # tells ERPNext: use Stock Entry.custom_work_plan
    })

    # Show only Stock Entries linked to this Work Plan
    data["transactions"].append({
        "items": ["Stock Entry"]  # Stock Entries linked via custom_work_plan
    })

    return data
