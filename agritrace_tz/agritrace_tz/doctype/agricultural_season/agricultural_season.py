import frappe
from frappe.model.document import Document


class AgriculturalSeason(Document):

    def validate(self):
        self.validate_farmer()
        self.validate_season_dates()

    def validate_farmer(self):
        if not frappe.db.exists("Farmer", self.farmer):
            frappe.throw("The selected Farmer does not exist.")

        farmer_status = frappe.db.get_value(
            "Farmer",
            self.farmer,
            "status"
        )

        if farmer_status != "Active":
            frappe.throw(
                "You can only register an Agricultural Season "
                "under an active Farmer."
            )

    def validate_season_dates(self):
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                frappe.throw(
                    "End Date must be later than Start Date."
                )