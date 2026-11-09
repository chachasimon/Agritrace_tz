// Copyright (c) 2026, aakvatech limited and contributors
// For license information, please see license.txt

frappe.query_reports["AgriTrace Farm Financial Performance Report"] = {
    filters: [
        {
            fieldname: "farmer",
            label: __("Farmer"),
            fieldtype: "Link",
            options: "Farmer"
        },
        {
            fieldname: "farm",
            label: __("Farm"),
            fieldtype: "Link",
            options: "Farm"
        },
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date"
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date"
        }
    ]
};