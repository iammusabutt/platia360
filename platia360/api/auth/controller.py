# In your ERPNext app e.g. platia360/api/auth/sso_login.py
import frappe
from frappe.utils import get_url

@frappe.whitelist(allow_guest=True)
def sso_login(token):
    # Call your existing identity() function internally
    result = frappe.get_attr("platia360.api.auth.jwt.middleware.identity")()
    
    # identity() will set the session (since it's in this same request)
    if result.get("status") == "success":
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/app"
    else:
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = f"/login?error={result.get('error')}"
