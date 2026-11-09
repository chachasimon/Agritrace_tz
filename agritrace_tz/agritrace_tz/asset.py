import frappe


def validate_asset(doc, method=None):

    # Skip standard ERPNext assets
    if not doc.custom_is_agritrace_equipment:
        return

    # Farmer is required
    if not doc.custom_farmer:
        frappe.throw("Please select a Farmer.")

    # Farm is required
    if not doc.custom_farm:
        frappe.throw("Please select a Farm.")

    # Check Farmer exists
    if not frappe.db.exists("Farmer", doc.custom_farmer):
        frappe.throw("The selected Farmer does not exist.")

    # Check Farm exists
    if not frappe.db.exists("Farm", doc.custom_farm):
        frappe.throw("The selected Farm does not exist.")

    # Get Farmer associated with Farm
    farm_farmer = frappe.db.get_value(
        "Farm",
        doc.custom_farm,
        "farmer"
    )

    # Ensure Farm belongs to Farmer
    if farm_farmer != doc.custom_farmer:
        frappe.throw(
            "The selected Farm does not belong to the selected Farmer."
        )

    # Equipment condition is required
    if not doc.custom_equipment_condition:
        frappe.throw("Please select the Equipment Condition.")