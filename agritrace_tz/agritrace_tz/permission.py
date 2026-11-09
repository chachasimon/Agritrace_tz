import frappe


# Shared reference DocTypes available to Farmers as read-only data.
SHARED_READ_ONLY_DOCTYPES = {
    "Crop",
    "Farm Activity Type",
}


# Actions allowed to a Farmer on their own business records.
FARMER_ALLOWED_PERMISSIONS = {
    "read",
    "write",
    "create",
    "submit",
    "print",
    "email",
    "export",
}


def is_privileged_user(user):
    user = user or frappe.session.user

    if user == "Administrator":
        return True

    roles = frappe.get_roles(user)

    return (
        "System Manager" in roles
        or "AgriTrace Manager" in roles
    )


def get_linked_farmer(user):
    user = user or frappe.session.user

    if not user or user == "Guest":
        return None

    return frappe.db.get_value(
        "Farmer",
        {"user_account": user},
        "name"
    )


def get_ownership_fields(doctype):
    meta = frappe.get_meta(doctype)
    fieldnames = {field.fieldname for field in meta.fields}

    farmer_field = (
        "farmer" if "farmer" in fieldnames
        else "custom_farmer" if "custom_farmer" in fieldnames
        else None
    )

    farm_field = (
        "farm" if "farm" in fieldnames
        else "custom_farm" if "custom_farm" in fieldnames
        else None
    )

    return farmer_field, farm_field


def get_document_farmer(doc):
    """Resolve document ownership through Farmer and/or Farm."""

    farmer_field, farm_field = get_ownership_fields(doc.doctype)

    farmer = doc.get(farmer_field) if farmer_field else None
    farm = doc.get(farm_field) if farm_field else None

    farm_farmer = None

    if farm:
        farm_farmer = frappe.db.get_value("Farm", farm, "farmer")

        if not farm_farmer:
            return None

    if farmer and farm_farmer and farmer != farm_farmer:
        return None

    return farmer or farm_farmer


def validate_document_ownership(doc, method=None):
    """
    Enforce ownership for Farmer business documents.
    Supplier and Customer retain their dedicated party.py validation.
    """

    user = frappe.session.user

    if is_privileged_user(user):
        return

    if not user or user == "Guest":
        return

    if "Farmer" not in frappe.get_roles(user):
        return

    if doc.doctype in (
        "Farmer",
        "Supplier",
        "Customer",
        "Crop",
        "Farm Activity Type",
    ):
        return

    farmer = get_linked_farmer(user)

    if not farmer:
        frappe.throw(
            "Your user account is not linked to a Farmer record."
        )

    farmer_field, farm_field = get_ownership_fields(doc.doctype)

    if not farmer_field and not farm_field:
        return

    # Assign the logged-in Farmer when the document supports direct ownership.
    if farmer_field and not doc.get(farmer_field):
        doc.set(farmer_field, farmer)

    # Reject direct ownership belonging to another Farmer.
    if farmer_field and doc.get(farmer_field) != farmer:
        frappe.throw(
            "You can only create or manage records belonging "
            "to your own Farmer account."
        )

    # Validate Farm ownership whenever a Farm is selected.
    if farm_field:
        farm = doc.get(farm_field)

        if farm:
            farm_farmer = frappe.db.get_value(
                "Farm",
                farm,
                "farmer"
            )

            if not farm_farmer:
                frappe.throw("The selected Farm does not have a valid Farmer.")

            if farm_farmer != farmer:
                frappe.throw(
                    "You cannot use a Farm belonging to another Farmer."
                )

            # Derive direct Farmer ownership where applicable.
            if farmer_field and doc.get(farmer_field) != farm_farmer:
                frappe.throw(
                    "The selected Farmer and Farm do not belong together."
                )

    # Farm-only documents must have a valid Farm.
    if not farmer_field and farm_field and not doc.get(farm_field):
        frappe.throw("A Farm must be selected for this record.")

    # Prevent records with ownership fields from being saved unowned.
    if not get_document_farmer(doc):
        frappe.throw(
            "This record must be linked to your Farmer account or Farm."
        )


def get_farmer_permission_query(doctype, user=None):
    user = user or frappe.session.user

    if is_privileged_user(user):
        return ""

    if not user or user == "Guest":
        return "1=0"

    roles = frappe.get_roles(user)

    if "Farmer" not in roles:
        return ""

    if doctype in SHARED_READ_ONLY_DOCTYPES:
        return "1=1"

    farmer = get_linked_farmer(user)

    if not farmer:
        return "1=0"

    if doctype == "Farmer":
        return (
            f"`tabFarmer`.`user_account` = "
            f"{frappe.db.escape(user)}"
        )

    farmer_field, farm_field = get_ownership_fields(doctype)

    table = f"`tab{doctype}`"
    escaped_farmer = frappe.db.escape(farmer)

    direct_condition = None
    farm_condition = None

    if farmer_field:
        direct_condition = (
            f"{table}.`{farmer_field}` = {escaped_farmer}"
        )

    if farm_field:
        farm_condition = (
            "EXISTS ("
            "SELECT 1 FROM `tabFarm` AS farm_link "
            f"WHERE farm_link.name = {table}.`{farm_field}` "
            f"AND farm_link.farmer = {escaped_farmer}"
            ")"
        )

    if direct_condition and farm_condition:
        return (
            f"(({table}.`{farmer_field}` IS NULL "
            f"OR {table}.`{farmer_field}` = '') "
            f"AND ({farm_condition}) "
            f"OR ({direct_condition} "
            f"AND ({table}.`{farm_field}` IS NULL "
            f"OR {table}.`{farm_field}` = '' "
            f"OR {farm_condition})))"
        )

    if direct_condition:
        return direct_condition

    if farm_condition:
        return farm_condition

    return "1=0"


def has_farmer_permission(doc, user=None, ptype=None):
    user = user or frappe.session.user
    ptype = ptype or "read"

    # Privileged users have full access.
    if is_privileged_user(user):
        return True

    if not user or user == "Guest":
        return False

    roles = frappe.get_roles(user)

    # Non-Farmer users use standard Frappe permissions.
    if "Farmer" not in roles:
        return None

    # Shared reference data is read-only.
    if doc.doctype in SHARED_READ_ONLY_DOCTYPES:
        return ptype == "read"

    # Farmer master is read-only and restricted to its owner.
    if doc.doctype == "Farmer":
        return (
            ptype == "read"
            and doc.user_account == user
        )

    # Restrict Farmers to the allowed permission types.
    if ptype not in FARMER_ALLOWED_PERMISSIONS:
        return False

    # Get the Farmer linked to the logged-in user.
    farmer = get_linked_farmer(user)

    if not farmer:
        return False

    # New documents:
    # Allow the controller check for creation to pass.
    # Frappe Role Permissions will still determine
    # whether the user can actually create the document.
    if doc.is_new():
        farmer_field, farm_field = get_ownership_fields(doc.doctype)

        if farmer_field or farm_field:
            return ptype == "create"

        return False

    # Existing documents must belong to the logged-in Farmer.
    return get_document_farmer(doc) == farmer

def get_query_for(doctype):
    def query(user=None):
        return get_farmer_permission_query(doctype, user)

    return query


def get_farmer_query(user=None):
    return get_farmer_permission_query("Farmer", user)


def get_farm_query(user=None):
    return get_farmer_permission_query("Farm", user)


def get_farm_plot_query(user=None):
    return get_farmer_permission_query("Farm Plot", user)


def get_agricultural_season_query(user=None):
    return get_farmer_permission_query("Agricultural Season", user)


def get_crop_cycle_query(user=None):
    return get_farmer_permission_query("Crop Cycle", user)


def get_agricultural_activity_query(user=None):
    return get_farmer_permission_query("Agricultural Activity", user)


def get_farm_worker_query(user=None):
    return get_farmer_permission_query("Farm Worker", user)

def get_supplier_query(user=None):
    return get_farmer_permission_query("Supplier", user)


def get_customer_query(user=None):
    return get_farmer_permission_query("Customer", user)

def get_farm_worker_payment_query(user=None):
    return get_farmer_permission_query("Farm Worker Payment", user)


def get_farm_budget_query(user=None):
    return get_farmer_permission_query("Farm Budget", user)


def get_farm_expense_query(user=None):
    return get_farmer_permission_query("Farm Expense", user)


def get_farm_income_query(user=None):
    return get_farmer_permission_query("Farm Income", user)


def get_harvest_record_query(user=None):
    return get_farmer_permission_query("Harvest Record", user)


def get_soil_test_query(user=None):
    return get_farmer_permission_query("Soil Test", user)


def get_irrigation_records_query(user=None):
    return get_farmer_permission_query("Irrigation Records", user)


def get_work_record_query(user=None):
    return get_farmer_permission_query("Work Record", user)


def get_produce_loss_record_query(user=None):
    return get_farmer_permission_query("Produce Loss Record", user)


def get_produce_quality_inspection_query(user=None):
    return get_farmer_permission_query("Produce Quality Inspection", user)


def get_paste_and_disease_observation_query(user=None):
    return get_farmer_permission_query("Paste And Disease Observation", user)


def get_farm_equipment_usage_query(user=None):
    return get_farmer_permission_query("Farm Equipment Usage", user)


def get_farm_worker_assignment_query(user=None):
    return get_farmer_permission_query("Farm Worker Assignment", user)


def get_farm_activity_query(user=None):
    return get_farmer_permission_query("Farm Activity", user)


def get_crop_query(user=None):
    return get_farmer_permission_query("Crop", user)


def get_farm_activity_type_query(user=None):
    return get_farmer_permission_query("Farm Activity Type", user)


def get_warehouse_query(user=None):
    return get_farmer_permission_query("Warehouse", user)


def get_asset_query(user=None):
    return get_farmer_permission_query("Asset", user)


def get_asset_repair_query(user=None):
    return get_farmer_permission_query("Asset Repair", user)


def get_asset_maintenance_query(user=None):
    return get_farmer_permission_query("Asset Maintenance", user)


def get_asset_maintenance_log_query(user=None):
    return get_farmer_permission_query("Asset Maintenance Log", user)


def get_material_request_query(user=None):
    return get_farmer_permission_query("Material Request", user)


def get_purchase_order_query(user=None):
    return get_farmer_permission_query("Purchase Order", user)


def get_purchase_receipt_query(user=None):
    return get_farmer_permission_query("Purchase Receipt", user)


def get_purchase_invoice_query(user=None):
    return get_farmer_permission_query("Purchase Invoice", user)


def get_stock_entry_query(user=None):
    return get_farmer_permission_query("Stock Entry", user)


def get_sales_order_query(user=None):
    return get_farmer_permission_query("Sales Order", user)


def get_sales_invoice_query(user=None):
    return get_farmer_permission_query("Sales Invoice", user)
