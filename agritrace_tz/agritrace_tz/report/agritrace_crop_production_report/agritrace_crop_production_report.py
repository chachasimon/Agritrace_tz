# Copyright (c) 2026, aakvatech limited and contributors
# For license information, please see license.txt
import frappe
from frappe import _


def execute(filters=None):
    filters = frappe._dict(filters or {})

    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns():
    return [
        {
            "label": _("Harvest Record"),
            "fieldname": "harvest_record",
            "fieldtype": "Link",
            "options": "Harvest Record",
            "width": 160
        },
        {
            "label": _("Harvest Reference"),
            "fieldname": "harvest_reference",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Farmer"),
            "fieldname": "farmer",
            "fieldtype": "Link",
            "options": "Farmer",
            "width": 140
        },
        {
            "label": _("Farm"),
            "fieldname": "farm",
            "fieldtype": "Link",
            "options": "Farm",
            "width": 140
        },
        {
            "label": _("Crop Cycle"),
            "fieldname": "crop_cycle",
            "fieldtype": "Link",
            "options": "Crop Cycle",
            "width": 150
        },
        {
            "label": _("Harvest Date"),
            "fieldname": "harvest_date",
            "fieldtype": "Date",
            "width": 110
        },
        {
            "label": _("Produce Grade"),
            "fieldname": "produce_grade",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Quantity"),
            "fieldname": "quantity",
            "fieldtype": "Float",
            "width": 110
        },
        {
            "label": _("UOM"),
            "fieldname": "uom",
            "fieldtype": "Link",
            "options": "UOM",
            "width": 90
        },
        {
            "label": _("Total Harvest Quantity"),
            "fieldname": "total_quantity",
            "fieldtype": "Float",
            "width": 150
        }
    ]


def get_data(filters):
    conditions = []

    for field in ["farmer", "farm", "crop_cycle"]:
        if filters.get(field):
            conditions.append([
                field,
                "=",
                filters.get(field)
            ])

    if filters.get("from_date"):
        conditions.append([
            "harvest_date",
            ">=",
            filters.get("from_date")
        ])

    if filters.get("to_date"):
        conditions.append([
            "harvest_date",
            "<=",
            filters.get("to_date")
        ])

    harvest_records = frappe.get_list(
        "Harvest Record",
        filters=conditions,
        fields=[
            "name",
            "harvest_reference",
            "farmer",
            "farm",
            "crop_cycle",
            "harvest_date",
            "total_quantity"
        ],
        order_by="harvest_date desc"
    )

    if not harvest_records:
        return []

    record_names = [
        record.name for record in harvest_records
    ]

    query = """
        SELECT
            parent,
            produce_grade,
            quantity,
            uom,
            idx
        FROM `tabHarvest Detail`
        WHERE parent IN %(record_names)s
          AND parenttype = 'Harvest Record'
          AND parentfield = 'harvest_detail'
    """

    values = {
        "record_names": tuple(record_names)
    }

    if filters.get("produce_grade"):
        query += """
            AND produce_grade = %(produce_grade)s
        """
        values["produce_grade"] = filters.get("produce_grade")

    query += " ORDER BY parent ASC, idx ASC"

    harvest_details = frappe.db.sql(
        query,
        values,
        as_dict=True
    )

    details_by_parent = {}

    for detail in harvest_details:
        details_by_parent.setdefault(
            detail.parent,
            []
        ).append(detail)

    data = []

    for record in harvest_records:
        details = details_by_parent.get(
            record.name,
            []
        )

        for detail in details:
            data.append([
                record.name,
                record.harvest_reference,
                record.farmer,
                record.farm,
                record.crop_cycle,
                record.harvest_date,
                detail.produce_grade,
                detail.quantity,
                detail.uom,
                record.total_quantity
            ])

    return data