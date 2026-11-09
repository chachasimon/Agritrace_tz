# Copyright (c) 2026, aakvatech limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Farmer(Document):

    def validate(self):
        if "AgriTrace Manager" not in frappe.get_roles():
            if self.user_account != frappe.session.user:
                frappe.throw(
                    "You can only register a Farmer profile for your own account."
                )

        self.validate_user_account()

    def validate_user_account(self):

        # Check whether the user account exists
        if not frappe.db.exists("User", self.user_account):
            frappe.throw("The selected User Account does not exist.")

        # Check whether the user account is enabled
        user_enabled = frappe.db.get_value(
            "User",
            self.user_account,
            "enabled"
        )

        if not user_enabled:
            frappe.throw("The selected User Account is disabled.")

        # Prevent one user from being assigned to multiple farmers
        existing_farmer = frappe.db.exists(
            "Farmer",
            {
                "user_account": self.user_account,
                "name": ["!=", self.name]
            }
        )

        if existing_farmer:
            frappe.throw(
                "This User Account is already assigned to another Farmer."
            )
