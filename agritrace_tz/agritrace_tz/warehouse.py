import frappe


def validate_warehouse(doc, method=None):

    # Group warehouses do not require Farmer or Farm
    if doc.is_group:
        return

    # Standard ERPNext warehouses are not validated by AgriTrace
    if not doc.custom_is_agritrace_warehouse:
        return

    # AgriTrace warehouses must have a Farmer
    if not doc.custom_farmer:
        frappe.throw("Please select a Farmer for this AgriTrace warehouse.")

    # AgriTrace warehouses must have a Farm
    if not doc.custom_farm:
        frappe.throw("Please select a Farm for this AgriTrace warehouse.")

    # Check whether the Farmer exists
    if not frappe.db.exists("Farmer", doc.custom_farmer):
        frappe.throw("The selected Farmer does not exist.")

    # Check whether the Farm exists
    if not frappe.db.exists("Farm", doc.custom_farm):
        frappe.throw("The selected Farm does not exist.")

    # Retrieve the Farmer associated with the selected Farm
    farm_farmer = frappe.db.get_value(
        "Farm",
        doc.custom_farm,
        "farmer"
    )

    # Ensure that the Farm belongs to the selected Farmer
    if farm_farmer != doc.custom_farmer:
        frappe.throw(
            "The selected Farm does not belong to the selected Farmer."
        )