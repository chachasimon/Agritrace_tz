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
            "label": _("Farmer"),
            "fieldname": "farmer",
            "fieldtype": "Link",
            "options": "Farmer",
            "width": 160
        },
        {
            "label": _("Farm"),
            "fieldname": "farm",
            "fieldtype": "Link",
            "options": "Farm",
            "width": 160
        },
        {
            "label": _("Total Income"),
            "fieldname": "total_income",
            "fieldtype": "Currency",
            "width": 140
        },
        {
            "label": _("Total Expenses"),
            "fieldname": "total_expenses",
            "fieldtype": "Currency",
            "width": 140
        },
        {
            "label": _("Net Profit"),
            "fieldname": "net_profit",
            "fieldtype": "Currency",
            "width": 140
        },
        {
            "label": _("Profit Margin"),
            "fieldname": "profit_margin",
            "fieldtype": "Percent",
            "width": 120
        },
        {
            "label": _("Income Transactions"),
            "fieldname": "income_count",
            "fieldtype": "Int",
            "width": 140
        },
        {
            "label": _("Expense Transactions"),
            "fieldname": "expense_count",
            "fieldtype": "Int",
            "width": 140
        }
    ]


def get_data(filters):
    income_conditions = []
    expense_conditions = []

    for field in ["farmer", "farm"]:
        if filters.get(field):
            income_conditions.append(
                [field, "=", filters.get(field)]
            )
            expense_conditions.append(
                [field, "=", filters.get(field)]
            )

    if filters.get("from_date"):
        income_conditions.append([
            "income_date", ">=", filters.get("from_date")
        ])

        expense_conditions.append([
            "expense_date", ">=", filters.get("from_date")
        ])

    if filters.get("to_date"):
        income_conditions.append([
            "income_date", "<=", filters.get("to_date")
        ])

        expense_conditions.append([
            "expense_date", "<=", filters.get("to_date")
        ])

    incomes = frappe.get_list(
        "Farm Income",
        filters=income_conditions,
        fields=["farmer", "farm", "amount"],
    )

    expenses = frappe.get_list(
        "Farm Expense",
        filters=expense_conditions,
        fields=["farmer", "farm", "amount"],
    )

    financial_data = {}

    for income in incomes:
        key = (income.farmer, income.farm)

        if key not in financial_data:
            financial_data[key] = {
                "total_income": 0,
                "total_expenses": 0,
                "income_count": 0,
                "expense_count": 0
            }

        financial_data[key]["total_income"] += income.amount or 0
        financial_data[key]["income_count"] += 1

    for expense in expenses:
        key = (expense.farmer, expense.farm)

        if key not in financial_data:
            financial_data[key] = {
                "total_income": 0,
                "total_expenses": 0,
                "income_count": 0,
                "expense_count": 0
            }

        financial_data[key]["total_expenses"] += expense.amount or 0
        financial_data[key]["expense_count"] += 1

    data = []

    for (farmer, farm), values in financial_data.items():
        total_income = values["total_income"]
        total_expenses = values["total_expenses"]

        net_profit = total_income - total_expenses

        profit_margin = (
            (net_profit / total_income) * 100
            if total_income else 0
        )

        data.append([
            farmer,
            farm,
            total_income,
            total_expenses,
            net_profit,
            profit_margin,
            values["income_count"],
            values["expense_count"]
        ])

    data.sort(key=lambda row: row[4], reverse=True)

    return data