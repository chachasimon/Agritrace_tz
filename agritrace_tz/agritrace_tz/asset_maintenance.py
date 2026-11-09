import frappe


def validate_asset_maintenance(doc, method=None):
    if not doc.asset_name:
        frappe.throw("Please select an Asset.")

    asset = frappe.db.get_value(
        "Asset",
        doc.asset_name,
        [
            "custom_is_agritrace_equipment",
            "custom_farmer",
            "custom_farm"
        ],
        as_dict=True
    )

    if not asset:
        frappe.throw("The selected Asset does not exist.")

    # Standard ERPNext assets are not restricted by AgriTrace
    if not asset.custom_is_agritrace_equipment:
        return

    if not asset.custom_farmer or not asset.custom_farm:
        frappe.throw(
            "The selected AgriTrace equipment must have a Farmer and Farm."
        )

    # Automatically synchronize ownership from the Asset
    doc.custom_farmer = asset.custom_farmer
    doc.custom_farm = asset.custom_farm