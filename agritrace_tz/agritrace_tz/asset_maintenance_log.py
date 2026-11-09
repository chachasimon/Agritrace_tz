import frappe


def validate_asset_maintenance_log(doc, method=None):
    if not doc.asset_maintenance:
        frappe.throw("Please select an Asset Maintenance record.")

    maintenance = frappe.db.get_value(
        "Asset Maintenance",
        doc.asset_maintenance,
        ["custom_farmer", "custom_farm", "asset_name"],
        as_dict=True
    )

    if not maintenance:
        frappe.throw("The selected Asset Maintenance record does not exist.")

    if not maintenance.asset_name:
        frappe.throw("The Asset Maintenance record has no linked Asset.")

    asset = frappe.db.get_value(
        "Asset",
        maintenance.asset_name,
        ["custom_is_agritrace_equipment", "custom_farmer", "custom_farm"],
        as_dict=True
    )

    if not asset:
        frappe.throw("The linked Asset does not exist.")

    if not asset.custom_is_agritrace_equipment:
        return

    if not asset.custom_farmer or not asset.custom_farm:
        frappe.throw("The AgriTrace equipment must have a Farmer and Farm.")

    doc.custom_farmer = asset.custom_farmer
    doc.custom_farm = asset.custom_farm

    # Validate linked Purchase Invoice
    if doc.custom_purchase_invoice:
        invoice = frappe.db.get_value(
            "Purchase Invoice",
            doc.custom_purchase_invoice,
            ["custom_farmer", "custom_farm"],
            as_dict=True
        )

        if not invoice:
            frappe.throw("The selected Purchase Invoice does not exist.")

        if invoice.custom_farmer != doc.custom_farmer:
            frappe.throw(
                "The Purchase Invoice does not belong to this equipment's Farmer."
            )

        if invoice.custom_farm != doc.custom_farm:
            frappe.throw(
                "The Purchase Invoice does not belong to this equipment's Farm."
            )