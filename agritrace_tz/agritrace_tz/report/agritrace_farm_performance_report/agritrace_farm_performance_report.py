import frappe
from frappe import _
from frappe.utils import date_diff, today


def execute(filters=None):
    filters = frappe._dict(filters or {})

    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns():
    return [
        {
            "label": _("Crop Cycle"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Crop Cycle",
            "width": 160
        },
        {
            "label": _("Farmer"),
            "fieldname": "farmer",
            "fieldtype": "Link",
            "options": "Farmer",
            "width": 150
        },
        {
            "label": _("Farm"),
            "fieldname": "farm",
            "fieldtype": "Link",
            "options": "Farm",
            "width": 150
        },
        {
            "label": _("Plot"),
            "fieldname": "plot",
            "fieldtype": "Link",
            "options": "Farm Plot",
            "width": 120
        },
        {
            "label": _("Crop"),
            "fieldname": "crop",
            "fieldtype": "Link",
            "options": "Crop",
            "width": 130
        },
        {
            "label": _("Season"),
            "fieldname": "agricultural_season",
            "fieldtype": "Link",
            "options": "Agricultural Season",
            "width": 140
        },
        {
            "label": _("Planting Date"),
            "fieldname": "planting_date",
            "fieldtype": "Date",
            "width": 110
        },
        {
            "label": _("Expected Harvest"),
            "fieldname": "expected_harvest_date",
            "fieldtype": "Date",
            "width": 130
        },
        {
            "label": _("Actual Harvest"),
            "fieldname": "actual_harvest_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Days to Expected Harvest"),
            "fieldname": "days_to_harvest",
            "fieldtype": "Int",
            "width": 150
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 110
        }
    ]


def get_data(filters):
    conditions = {}

    for field in ["farmer", "farm", "crop", "status"]:
        if filters.get(field):
            conditions[field] = filters.get(field)

    records = frappe.get_list(
        "Crop Cycle",
        filters=conditions,
        fields=[
            "name",
            "farmer",
            "farm",
            "plot",
            "crop",
            "agricultural_season",
            "planting_date",
            "expected_harvest_date",
            "actual_harvest_date",
            "status"
        ],
        order_by="planting_date desc"
    )

    data = []

    for row in records:
        days_to_harvest = None

        if row.expected_harvest_date:
            days_to_harvest = date_diff(
                row.expected_harvest_date,
                today()
            )

        data.append([
            row.name,
            row.farmer,
            row.farm,
            row.plot,
            row.crop,
            row.agricultural_season,
            row.planting_date,
            row.expected_harvest_date,
            row.actual_harvest_date,
            days_to_harvest,
            row.status
        ])

    return data