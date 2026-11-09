import frappe


def validate_asset_repair(doc, method=None):

    # Check that Asset is selected
    if not doc.asset:
        frappe.throw("Please select an Asset.")

    # Retrieve Asset ownership information
    asset = frappe.db.get_value(
        "Asset",
        doc.asset,
        [
            "custom_is_agritrace_equipment",
            "custom_farmer",
            "custom_farm"
        ],
        as_dict=True
    )

    if not asset:
        frappe.throw("The selected Asset does not exist.")

    # Standard ERPNext assets are not validated by AgriTrace
    if not asset.custom_is_agritrace_equipment:
        return

    # Farmer and Farm are required
    if not doc.custom_farmer:
        frappe.throw("Please select a Farmer.")

    if not doc.custom_farm:
        frappe.throw("Please select a Farm.")

    # Ensure Farmer matches Asset ownership
    if doc.custom_farmer != asset.custom_farmer:
        frappe.throw(
            "The selected Farmer does not match the Asset owner."
        )

    # Ensure Farm matches Asset ownership
    if doc.custom_farm != asset.custom_farm:
        frappe.throw(
            "The selected Farm does not match the Asset's Farm."
        )