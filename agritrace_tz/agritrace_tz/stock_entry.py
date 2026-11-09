import frappe


def validate_stock_entry(doc, method=None):

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

    # Get Farmer associated with the Farm
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

    # Validate warehouse ownership
    def validate_warehouse(warehouse_name):

        if not warehouse_name:
            return

        warehouse = frappe.db.get_value(
            "Warehouse",
            warehouse_name,
            [
                "custom_is_agritrace_warehouse",
                "custom_farmer",
                "custom_farm"
            ],
            as_dict=True
        )

        if not warehouse:
            frappe.throw(
                f"The selected Warehouse {warehouse_name} does not exist."
            )

        # Allow standard ERPNext warehouses
        if not warehouse.custom_is_agritrace_warehouse:
            return

        # Check Farmer ownership
        if warehouse.custom_farmer != doc.custom_farmer:
            frappe.throw(
                "The selected Warehouse does not belong to this Farmer."
            )

        # Check Farm ownership
        if warehouse.custom_farm != doc.custom_farm:
            frappe.throw(
                "The selected Warehouse does not belong to this Farm."
            )

    # Validate parent-level warehouses
    validate_warehouse(doc.from_warehouse)
    validate_warehouse(doc.to_warehouse)

    # Validate item-row warehouses
    for row in doc.get("items", []):

        validate_warehouse(row.s_warehouse)
        validate_warehouse(row.t_warehouse)