import frappe
from frappe import _


def validate_sales_order(doc, method=None):
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

    if farm_farmer != doc.custom_farmer:
        frappe.throw(
            _("Farm {0} does not belong to Farmer {1}.").format(
                doc.custom_farm,
                doc.custom_farmer
            )
        )


def validate_items(doc):
    if not doc.items:
        frappe.throw(_("Please add at least one item."))

    for row in doc.items:
        validate_item_farmer(doc, row)
        validate_item_farm(doc, row)
        validate_item_crop_cycle(doc, row)


def validate_item_farmer(doc, row):
    if not row.custom_farmer:
        frappe.throw(
            _("Please select Farmer for Item {0}.").format(row.item_code)
        )

    if row.custom_farmer != doc.custom_farmer:
        frappe.throw(
            _("Item {0}: Farmer must match the Sales Order Farmer.").format(
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
            _("Item {0}: Farm must match the Sales Order Farm.").format(
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


def validate_item_crop_cycle(doc, row):
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