import frappe


def validate_purchase_receipt(doc, method=None):

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

        # Standard ERPNext warehouses are allowed
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

    # Validate the default warehouse
    validate_warehouse(doc.set_warehouse)

    # Validate item warehouses and linked Purchase Orders
    for row in doc.get("items", []):

        # Validate item warehouse
        validate_warehouse(row.warehouse)

        # Validate linked Purchase Order
        if row.purchase_order:

            purchase_order = frappe.db.get_value(
                "Purchase Order",
                row.purchase_order,
                [
                    "custom_farmer",
                    "custom_farm"
                ],
                as_dict=True
            )

            if not purchase_order:
                frappe.throw(
                    f"Purchase Order {row.purchase_order} does not exist."
                )

            if purchase_order.custom_farmer != doc.custom_farmer:
                frappe.throw(
                    "The linked Purchase Order belongs to another Farmer."
                )

            if purchase_order.custom_farm != doc.custom_farm:
                frappe.throw(
                    "The linked Purchase Order belongs to another Farm."
                )