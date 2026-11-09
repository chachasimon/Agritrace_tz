import frappe
from frappe.utils import getdate
from frappe.model.document import Document


class CropCycle(Document):

    def validate(self):
        self.validate_farmer()
        self.validate_farm()
        self.validate_plot()
        self.validate_crop()
        self.validate_season()
        self.validate_dates()

    def validate_farmer(self):
        if not frappe.db.exists("Farmer", self.farmer):
            frappe.throw("The selected Farmer does not exist.")

        farmer_status = frappe.db.get_value(
            "Farmer", self.farmer, "status"
        )

        if farmer_status != "Active":
            frappe.throw("The selected Farmer is not active.")

    def validate_farm(self):
        farm = frappe.db.get_value(
            "Farm",
            self.farm,
            ["farmer", "status"],
            as_dict=True
        )

        if not farm:
            frappe.throw("The selected Farm does not exist.")

        if farm.farmer != self.farmer:
            frappe.throw(
                "The selected Farm does not belong to this Farmer."
            )

        if farm.status != "Active":
            frappe.throw("The selected Farm is not active.")

    def validate_plot(self):
        plot = frappe.db.get_value(
            "Farm Plot",
            self.plot,
            ["farm", "status"],
            as_dict=True
        )

        if not plot:
            frappe.throw("The selected Farm Plot does not exist.")

        if plot.farm != self.farm:
            frappe.throw(
                "The selected Plot does not belong to the selected Farm."
            )

        if plot.status != "Active":
            frappe.throw("The selected Plot is not active.")

    def validate_crop(self):
        crop_status = frappe.db.get_value(
            "Crop", self.crop, "is_active"
        )

        if crop_status is None:
            frappe.throw("The selected Crop does not exist.")

        if not crop_status:
            frappe.throw("The selected Crop is inactive.")

    def validate_season(self):
        season = frappe.db.get_value(
            "Agricultural Season",
            self.agricultural_season,
            ["farmer", "start_date", "end_date", "status"],
            as_dict=True
        )

        if not season:
            frappe.throw(
                "The selected Agricultural Season does not exist."
            )

        if season.farmer != self.farmer:
            frappe.throw(
                "The selected Agricultural Season does not belong "
                "to this Farmer."
            )

        if season.status == "Cancelled":
            frappe.throw(
                "You cannot create a Crop Cycle under a cancelled season."
            )

        planting_date = getdate(self.planting_date)
        season_start_date = getdate(season.start_date)

        if planting_date < season_start_date:
            frappe.throw(
                "Planting Date cannot be earlier than the Season Start Date."
            )

        if season.end_date:
            season_end_date = getdate(season.end_date)

            if planting_date > season_end_date:
                frappe.throw(
                    "Planting Date cannot be later than the Season End Date."
                )

    def validate_dates(self):
        planting_date = getdate(self.planting_date)

        if self.expected_harvest_date:
            expected_date = getdate(self.expected_harvest_date)

            if expected_date <= planting_date:
                frappe.throw(
                    "Expected Harvest Date must be later than Planting Date."
                )

        if self.actual_harvest_date:
            actual_date = getdate(self.actual_harvest_date)

            if actual_date < planting_date:
                frappe.throw(
                    "Actual Harvest Date cannot be earlier than Planting Date."
                )

            if self.status not in ["Harvesting", "Completed"]:
                frappe.throw(
                    "Actual Harvest Date can only be entered when the "
                    "Crop Cycle is Harvesting or Completed."
                )