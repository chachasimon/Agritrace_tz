// Copyright (c) 2026, aakvatech limited and contributors
// For license information, please see license.txt

frappe.query_reports["AgriTrace Crop Production Report"] = {
	filters: [
		// {
		// 	"fieldname": "my_filter",
		// 	"label": __("My Filter"),
		// 	"fieldtype": "Data",
		// 	"reqd": 1,
		// },
	],
};
frappe.query_reports["AgriTrace Crop Production Report"] = {
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
            fieldname: "crop_cycle",
            label: __("Crop Cycle"),
            fieldtype: "Link",
            options: "Crop Cycle"
        },
        {
            fieldname: "from_date",
            label: __("Harvest Date From"),
            fieldtype: "Date"
        },
        {
            fieldname: "to_date",
            label: __("Harvest Date To"),
            fieldtype: "Date"
        },
        {
            fieldname: "produce_grade",
            label: __("Produce Grade"),
            fieldtype: "Select",
            options: "\nGrade A\nGrade B\nGrade C\nRejected"
        }
    ]
};