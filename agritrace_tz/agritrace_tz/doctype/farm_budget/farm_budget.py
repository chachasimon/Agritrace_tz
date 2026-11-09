import frappe
from frappe.model.document import Document
from frappe.utils import flt


class FarmBudget(Document):

    def validate(self):
        self.validate_farmer()
        self.validate_farm()
        self.validate_season()
        self.validate_crop_cycle()
        self.validate_budget_dates()
        self.calculate_budget_totals()

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

    def validate_season(self):
        if self.agriculture_season:
            season_farmer = frappe.db.get_value(
                "Agricultural Season",
                self.agriculture_season,
                "farmer"
            )

            if season_farmer != self.farmer:
                frappe.throw(
                    "Selected Agricultural Season does not belong to the selected Farmer."
                )

    def validate_crop_cycle(self):
        if self.crop_cycle:
            cycle = frappe.db.get_value(
                "Crop Cycle",
                self.crop_cycle,
                ["farmer", "farm", "agricultural_season"],
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

            if (
                self.agriculture_season
                and cycle.agricultural_season != self.agriculture_season
            ):
                frappe.throw(
                    "Crop Cycle does not belong to the selected Agricultural Season."
                )

    def validate_budget_dates(self):
        if (
            self.budget_start_date
            and self.budget_end_date
            and self.budget_end_date < self.budget_start_date
        ):
            frappe.throw(
                "Budget End Date cannot be earlier than Budget Start Date."
            )

    def calculate_budget_totals(self):
        total_expense = 0
        total_income = 0

        for row in self.get("budget_table"):
            amount = flt(row.planned_amount)

            if amount < 0:
                frappe.throw(
                    "Planned Amount cannot be negative."
                )

            if row.budget_type == "Expense":
                total_expense += amount

            elif row.budget_type == "Income":
                total_income += amount

        self.total_planned_expense = total_expense
        self.total_planned_income = total_income