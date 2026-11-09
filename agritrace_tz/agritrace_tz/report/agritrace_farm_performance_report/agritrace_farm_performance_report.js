// Copyright (c) 2026, aakvatech limited and contributors
// For license information, please see license.txt

frappe.query_reports["AgriTrace Farm Performance Report"] = {
	filters: [
		// {
		// 	"fieldname": "my_filter",
		// 	"label": __("My Filter"),
		// 	"fieldtype": "Data",
		// 	"reqd": 1,
		// },
	],
};
frappe.query_reports["AgriTrace Farm Performance Report"] = {
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
            fieldname: "crop",
            label: __("Crop"),
            fieldtype: "Link",
            options: "Crop"
        },
        {
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Select",
            options: [
                "",
                "Planned",
                "Planted",
                "Growing",
                "Harvest",
                "Completed",
                "Cancelled"
            ]
        }
    ]
};