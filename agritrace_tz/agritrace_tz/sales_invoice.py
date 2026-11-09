import frappe
from frappe import _


def validate_sales_invoice(doc, method=None):
    validate_farmer(doc)
    validate_farm(doc)
    validate_items(doc)


def validate_farmer(doc):
    if not doc.custom_farmer:
        frappe.throw(_("Please select a Farmer."))

    farmer = frappe.db.get_value(
        "Farmer",
        doc.custom_farmer,
        ["status"],
        as_dict=True
    )

    if not farmer:
        frappe.throw(_("Selected Farmer does not exist."))

    if farmer.status != "Active":
        frappe.throw(_("Selected Farmer is not active."))


def validate_farm(doc):
    if not doc.custom_farm:
        frappe.throw(_("Please select a Farm."))

    farm_farmer = frappe.db.get_value(
        "Farm",
        doc.custom_farm,
        "farmer"
    )

    if not farm_farmer:
        frappe.throw(
            _("Selected Farm does not have a Farmer assigned.")
        )

    if farm_farmer != doc.custom_farmer:
        frappe.throw(
            _("Farm {0} does not belong to Farmer {1}.").format(
                doc.custom_farm,
                doc.custom_farmer
            )
        )
    user = frappe.session.user
    roles = frappe.get_roles(user)

    is_farmer = "Farmer" in roles and not (
        "System Manager" in roles
        or "AgriTrace Manager" in roles
        or user == "Administrator"
    )

    if is_farmer:
        linked_farmer = frappe.db.get_value(
            "Farmer",
            {"user_account": user},
            "name"
        )

        if doc.custom_farmer != linked_farmer:
            frappe.throw(
                _("You can only create Sales Invoices for your own farm.")
            )

def validate_items(doc):
    if not doc.items:
        frappe.throw(_("Please add at least one item."))

    for row in doc.items:
        validate_item_farmer(doc, row)
        validate_item_farm(doc, row)
        validate_item_crop_cycle(row)
        validate_harvest_record(row)


def validate_item_farmer(doc, row):
    if not row.custom_farmer:
        frappe.throw(
            _("Please select Farmer for Item {0}.").format(row.item_code)
        )

    if row.custom_farmer != doc.custom_farmer:
        frappe.throw(
            _("Item {0}: Farmer must match the Sales Invoice Farmer.").format(
                row.item_code
            )
        )


def validate_item_farm(doc, row):
    if not row.custom_farm:
        frappe.throw(
            _("Please select Farm for Item {0}.").format(row.item_code)
        )

    if row.custom_farm != doc.custom_farm:
        frappe.throw(
            _("Item {0}: Farm must match the Sales Invoice Farm.").format(
                row.item_code
            )
        )

    farm_farmer = frappe.db.get_value(
        "Farm",
        row.custom_farm,
        "farmer"
    )

    if farm_farmer != row.custom_farmer:
        frappe.throw(
            _("Item {0}: Selected Farm does not belong to its Farmer.").format(
                row.item_code
            )
        )


def validate_item_crop_cycle(row):
    if not row.custom_crop_cycle:
        frappe.throw(
            _("Please select Crop Cycle for Item {0}.").format(row.item_code)
        )

    cycle = frappe.db.get_value(
        "Crop Cycle",
        row.custom_crop_cycle,
        ["farmer", "farm", "crop"],
        as_dict=True
    )

    if not cycle:
        frappe.throw(_("Selected Crop Cycle does not exist."))

    if cycle.farmer != row.custom_farmer:
        frappe.throw(
            _("Item {0}: Crop Cycle belongs to another Farmer.").format(
                row.item_code
            )
        )

    if cycle.farm != row.custom_farm:
        frappe.throw(
            _("Item {0}: Crop Cycle belongs to another Farm.").format(
                row.item_code
            )
        )

    crop_item = frappe.db.get_value(
        "Crop",
        cycle.crop,
        "custom_item"
    )

    if crop_item != row.item_code:
        frappe.throw(
            _("Item {0} does not match the Crop linked to Crop Cycle {1}.").format(
                row.item_code,
                row.custom_crop_cycle
            )
        )


def validate_harvest_record(row):
    if not row.custom_harvest_record:
        frappe.throw(
            _("Please select Harvest Record for Item {0}.").format(
                row.item_code
            )
        )

    harvest = frappe.db.get_value(
        "Harvest Record",
        row.custom_harvest_record,
        [
            "farmer",
            "farm",
            "crop_cycle",
            "stock_entry",
            "total_quantity"
        ],
        as_dict=True
    )

    if not harvest:
        frappe.throw(_("Selected Harvest Record does not exist."))

    if harvest.farmer != row.custom_farmer:
        frappe.throw(
            _("Selected Harvest Record belongs to another Farmer.")
        )

    if harvest.farm != row.custom_farm:
        frappe.throw(
            _("Selected Harvest Record belongs to another Farm.")
        )

    if harvest.crop_cycle != row.custom_crop_cycle:
        frappe.throw(
            _("Selected Harvest Record belongs to another Crop Cycle.")
        )

    if not harvest.stock_entry:
        frappe.throw(
            _("Harvest Record {0} has no Stock Entry.").format(
                row.custom_harvest_record
            )
        )

    stock_entry_status = frappe.db.get_value(
        "Stock Entry",
        harvest.stock_entry,
        "docstatus"
    )

    if stock_entry_status != 1:
        frappe.throw(
            _("Stock Entry for Harvest Record {0} must be submitted first.").format(
                row.custom_harvest_record
            )
        )

    stock_item = frappe.db.get_value(
        "Stock Entry Detail",
        {
            "parent": harvest.stock_entry,
            "item_code": row.item_code
        },
        "item_code"
    )

    if not stock_item:
        frappe.throw(
            _("Item {0} is not found in the Stock Entry linked to Harvest Record {1}.").format(
                row.item_code,
                row.custom_harvest_record
            )
        )