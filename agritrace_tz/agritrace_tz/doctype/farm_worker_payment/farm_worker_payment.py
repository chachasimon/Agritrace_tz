import frappe
from frappe.model.document import Document
from frappe.utils import flt


class FarmWorkerPayment(Document):

    def validate(self):
        self.validate_farmer()
        self.validate_farm()
        self.validate_worker()
        self.validate_payment_period()
        self.validate_payment_amounts()
        self.calculate_payment_totals()

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

        if not farm_farmer:
            frappe.throw("Selected Farm has no assigned Farmer.")

        if farm_farmer != self.farmer:
            frappe.throw(
                "Selected Farm does not belong to the selected Farmer."
            )

    def validate_worker(self):
        if not self.worker:
            frappe.throw("Please select a Worker.")

        worker_farmer = frappe.db.get_value(
            "Farm Worker", self.worker, "farmer"
        )

        if not worker_farmer:
            frappe.throw("Selected Worker has no assigned Farmer.")

        if worker_farmer != self.farmer:
            frappe.throw(
                "Selected Worker does not belong to the selected Farmer."
            )

    def validate_payment_period(self):
        if (
            self.payment_period_start
            and self.payment_period_end
            and self.payment_period_end < self.payment_period_start
        ):
            frappe.throw(
                "Payment Period End cannot be earlier than Payment Period Start."
            )

    def validate_payment_amounts(self):
        amount_due = flt(self.amount_due)

        if amount_due < 0:
            frappe.throw("Amount Due cannot be negative.")

        total_paid = 0

        for entry in self.get("payment_entry"):
            amount = flt(entry.amount_paid)

            if amount < 0:
                frappe.throw("Amount Paid cannot be negative.")

            total_paid += amount

        if total_paid > amount_due:
            frappe.throw(
                "Total Amount Paid cannot exceed Amount Due."
            )

    def calculate_payment_totals(self):
        total_paid = sum(
            flt(entry.amount_paid)
            for entry in self.get("payment_entry")
        )

        self.amount_paid = total_paid
        self.balance = flt(self.amount_due) - total_paid

        if total_paid == 0:
            self.payment_status = "Unpaid"
        elif total_paid < flt(self.amount_due):
            self.payment_status = "Partially Paid"
        else:
            self.payment_status = "Paid"