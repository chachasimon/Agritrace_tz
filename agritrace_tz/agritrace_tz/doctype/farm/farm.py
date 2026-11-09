# Copyright (c) 2026, aakvatech limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Farm(Document):

    def validate(self):
        self.validate_farmer()
        self.validate_farm_size()

    def validate_farmer(self):
        # Ensure the selected Farmer exists
        if not frappe.db.exists("Farmer", self.farmer):
            frappe.throw("The selected Farmer does not exist.")

        # Ensure the Farmer is active
        farmer_status = frappe.db.get_value(
            "Farmer",
            self.farmer,
            "status"
        )

        if farmer_status != "Active":
            frappe.throw("You can only register a farm under an active Farmer.")

    def validate_farm_size(self):
        if self.total_size is not None and self.total_size <= 0:
            frappe.throw("Farm size must be greater than zero.")