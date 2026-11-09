import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate, today


class FarmExpense(Document):

    def validate(self):
        self.validate_farmer()
        self.validate_farm()
        self.validate_crop_cycle()
        self.validate_expense_date()
        self.validate_amount()

    def validate_farmer(self):
        if not self.farmer:
            frappe.throw("Please select a Farmer.")

        if not frappe.db.exists("Farmer", self.farmer):
            frappe.throw("Selected Farmer does not exist.")

    def validate_farm(self):
        if not self.farm:
            frappe.throw("Please select a Farm.")

        farm_farmer = frappe.db.get_value(
            "Farm", self.farm, "farmer"
        )

        if farm_farmer != self.farmer:
            frappe.throw(
                "Selected Farm does not belong to the selected Farmer."
            )

    def validate_crop_cycle(self):
        if self.crop_cycle:
            cycle = frappe.db.get_value(
                "Crop Cycle",
                self.crop_cycle,
                ["farmer", "farm"],
                as_dict=True
            )

            if not cycle:
                frappe.throw("Selected Crop Cycle does not exist.")

            if cycle.farmer != self.farmer:
                frappe.throw(
                    "Selected Crop Cycle belongs to another Farmer."
                )

            if cycle.farm != self.farm:
                frappe.throw(
                    "Selected Crop Cycle belongs to another Farm."
                )

    def validate_expense_date(self):
        if self.expense_date and getdate(self.expense_date) > getdate(today()):
            frappe.throw("Expense Date cannot be in the future.")

    def validate_amount(self):
        if flt(self.amount) <= 0:
            frappe.throw("Expense Amount must be greater than zero.")