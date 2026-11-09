import frappe


def validate_purchase_invoice(doc, method=None):
    user = frappe.session.user
    roles = frappe.get_roles(user)

    is_farmer = "Farmer" in roles and not (
        "System Manager" in roles
        or "AgriTrace Manager" in roles
        or user == "Administrator"
    )

    # Standard ERPNext invoices from other roles remain supported.
    if not doc.custom_farmer and not doc.custom_farm:
        if is_farmer:
            frappe.throw("Please select a Farmer and Farm.")
        return

    if not doc.custom_farmer:
        frappe.throw("Please select a Farmer.")

    if not doc.custom_farm:
        frappe.throw("Please select a Farm.")

    if not frappe.db.exists("Farmer", doc.custom_farmer):
        frappe.throw("The selected Farmer does not exist.")

    farm_farmer = frappe.db.get_value(
        "Farm",
        doc.custom_farm,
        "farmer"
    )

    if not farm_farmer:
        frappe.throw("The selected Farm does not exist.")

    if farm_farmer != doc.custom_farmer:
        frappe.throw(
            "The selected Farm does not belong to the selected Farmer."
        )

    # A Farmer can only create invoices for their own account.
    if is_farmer:
        linked_farmer = frappe.db.get_value(
            "Farmer",
            {"user_account": user},
            "name"
        )

        if doc.custom_farmer != linked_farmer:
            frappe.throw(
                "You can only create Purchase Invoices for your own farm."
            )