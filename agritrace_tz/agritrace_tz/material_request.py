import frappe


def validate_material_request(doc, method=None):

    # Validate only agricultural purchase requests
    if doc.material_request_type != "Purchase":
        return

    # Farmer is required
    if not doc.custom_farmer:
        frappe.throw("Please select a Farmer.")

    # Farm is required
    if not doc.custom_farm:
        frappe.throw("Please select a Farm.")

    # Check that Farmer exists
    if not frappe.db.exists("Farmer", doc.custom_farmer):
        frappe.throw("The selected Farmer does not exist.")

    # Check that Farm exists
    if not frappe.db.exists("Farm", doc.custom_farm):
        frappe.throw("The selected Farm does not exist.")

    # Get the Farmer associated with the Farm
    farm_farmer = frappe.db.get_value(
        "Farm",
        doc.custom_farm,
        "farmer"
    )

    # Ensure the Farm belongs to the selected Farmer
    if farm_farmer != doc.custom_farmer:
        frappe.throw(
            "The selected Farm does not belong to the selected Farmer."
        )

    # Validate the warehouse if one is selected
    if doc.set_warehouse:

        warehouse = frappe.db.get_value(
            "Warehouse",
            doc.set_warehouse,
            [
                "custom_is_agritrace_warehouse",
                "custom_farmer",
                "custom_farm"
            ],
            as_dict=True
        )

        if not warehouse:
            frappe.throw("The selected Warehouse does not exist.")

        # Standard ERPNext warehouses are not subject to AgriTrace checks
        if warehouse.custom_is_agritrace_warehouse:

            if warehouse.custom_farmer != doc.custom_farmer:
                frappe.throw(
                    "The selected Warehouse does not belong to this Farmer."
                )

            if warehouse.custom_farm != doc.custom_farm:
                frappe.throw(
                    "The selected Warehouse does not belong to this Farm."
                )