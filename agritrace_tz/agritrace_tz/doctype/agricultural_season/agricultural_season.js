// Copyright (c) 2026, aakvatech limited and contributors
// For license information, please see license.txt

frappe.ui.form.on("Agricultural Season", {
	validate(frm) {
		if (frm.doc.start_date && frm.doc.end_date) {
			if (frm.doc.end_date <= frm.doc.start_date) {
				frappe.throw(__("End Date must be later than Start Date."));
			}
		}
	},
});
