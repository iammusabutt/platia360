import frappe
from frappe import _

@frappe.whitelist()
def get_customer_sales_view(custom_int_ref=None, limit=100):
    """
    Fetches sales invoices + items from Customer_Sales_Total view
    Optionally filtered by custom_int_ref
    """
    query = """
        SELECT
            invoice_id,
            customer_id,
            customer_full_name,
            custom_int_ref,
            posting_date,
            due_date,
            grand_total,
            amount_in_words,
            item_code,
            item_name,
            qty,
            rate,
            amount
        FROM
            Customer_Sales_Total
        WHERE
            1=1
    """
    params = {}

    if custom_int_ref:
        query += " AND custom_int_ref = %(custom_int_ref)s"
        params["custom_int_ref"] = custom_int_ref

    query += " ORDER BY posting_date DESC LIMIT %(limit)s"
    params["limit"] = int(limit)

    data = frappe.db.sql(query, params, as_dict=True)

    return {
        "success": True,
        "rows": len(data),
        "data": data
    }

@frappe.whitelist(allow_guest=False)
def get_invoices_by_reference(reference):
    """
    Fetch Customer and Sales Invoices by custom integration reference.
    Example call:
    /api/method/silicon_signs.api.customer_invoices.get_invoices_by_reference?reference=123
    """

    if not reference:
        frappe.throw(_("Missing parameter: reference"))

    # Find the customer with given custom_int_ref
    customer = frappe.db.get_value(
        "Customer",
        {"custom_int_ref": reference},
        ["name", "customer_name", "custom_int_ref"],
        as_dict=True,
    )

    if not customer:
        frappe.throw(_("No customer found for reference: {0}").format(reference))

    # Get all sales invoices linked to this customer
    invoices = frappe.get_all(
        "Sales Invoice",
        filters={"customer": customer.name},
        fields=["name", "posting_date", "status", "grand_total", "outstanding_amount"],
        order_by="posting_date desc"
    )

    return {
        "customer": customer,
        "sales_invoices": invoices,
    }


@frappe.whitelist(allow_guest=False)
def get_customer_and_sales_data(customer=None, custom_integration_reference_=None):
    # 1) Build filters for Customer
    filters = {}

    if customer:
        filters["name"] = customer

    if custom_integration_reference_:
        filters["custom_integration_reference_"] = custom_integration_reference_

    # 2) Fetch filtered customers
    customers = frappe.get_all(
        "Customer",
        filters=filters,
        fields=[
            "name",
            "customer_name",
            "customer_group",
            "territory",
            "custom_integration_reference_"
        ]
    )

    # 3) Always define sales_orders (prevents NameError)
    sales_orders = []

    # 4) Only fetch Sales Orders if exactly one customer found
    if len(customers) == 1:
        customer_name = customers[0]["name"]
        sales_orders = frappe.get_all(
            "Sales Order",
            filters={"customer": customer_name},
            fields=["name", "customer", "transaction_date", "grand_total"]
        )

    # 5) Return both
    return {
        "customers": customers,
        "sales_orders": sales_orders
    }
