import frappe
from frappe.utils import flt
from frappe.model.document import Document


class AgriculturalActivity(Document):

    def validate(self):
        self.validate_farmer()
        self.validate_farm()
        self.validate_plot()
        self.validate_crop_cycle()
        self.validate_activity_type()
        self.validate_activity_inputs()
        self.validate_activity_workers()
        self.calculate_activity_costs()

    def validate_farmer(self):
        farmer_status = frappe.db.get_value(
            "Farmer",
            self.farmer,
            "status"
        )

        if farmer_status is None:
            frappe.throw("The selected Farmer does not exist.")

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
            self.farm_plot,
            ["farm", "status"],
            as_dict=True
        )

        if not plot:
            frappe.throw("The selected Farm Plot does not exist.")

        if plot.farm != self.farm:
            frappe.throw(
                "The selected Farm Plot does not belong to this Farm."
            )

        if plot.status != "Active":
            frappe.throw("The selected Farm Plot is not active.")

    def validate_crop_cycle(self):
        cycle = frappe.db.get_value(
            "Crop Cycle",
            self.crop_cycle,
            ["farmer", "farm", "plot", "status"],
            as_dict=True
        )

        if not cycle:
            frappe.throw("The selected Crop Cycle does not exist.")

        if cycle.farmer != self.farmer:
            frappe.throw(
                "The Crop Cycle does not belong to this Farmer."
            )

        if cycle.farm != self.farm:
            frappe.throw(
                "The Crop Cycle does not belong to this Farm."
            )

        if cycle.plot != self.farm_plot:
            frappe.throw(
                "The Crop Cycle does not belong to this Farm Plot."
            )

        if cycle.status == "Cancelled":
            frappe.throw(
                "You cannot record an activity under a cancelled Crop Cycle."
            )

    def validate_activity_type(self):
        is_active = frappe.db.get_value(
            "Farm Activity Type",
            self.activity_type,
            "is_active"
        )

        if is_active is None:
            frappe.throw(
                "The selected Farm Activity Type does not exist."
            )

        if not is_active:
            frappe.throw(
                "The selected Farm Activity Type is inactive."
            )

    def validate_activity_inputs(self):
        for row in self.activity_input:
            if flt(row.quantity) <= 0:
                frappe.throw(
                    f"Quantity must be greater than zero for input "
                    f"{row.input_name}."
                )

            if flt(row.unit_cost) < 0:
                frappe.throw(
                    f"Unit Cost cannot be negative for input "
                    f"{row.input_name}."
                )

    def validate_activity_workers(self):
        for row in self.activity_worker:

            if not row.worker_name:
                frappe.throw(
                    "Please select a Farm Worker."
                )

            worker_farmer = frappe.db.get_value(
                "Farm Worker",
                row.worker_name,
                "farmer"
            )

            if not worker_farmer:
                frappe.throw(
                    f"Worker {row.worker_name} does not have "
                    f"a registered Farmer."
                )

            if worker_farmer != self.farmer:
                frappe.throw(
                    f"Worker {row.worker_name} does not belong "
                    f"to Farmer {self.farmer}."
                )

            if flt(row.hours_worked) <= 0:
                frappe.throw(
                    f"Hours Worked must be greater than zero for worker "
                    f"{row.worker_name}."
                )

            if flt(row.wages) < 0:
                frappe.throw(
                    f"Wages cannot be negative for worker "
                    f"{row.worker_name}."
                )

    def calculate_activity_costs(self):
        total_input_cost = 0
        total_labour_cost = 0

        for row in self.activity_input:
            row.total_cost = flt(row.quantity) * flt(row.unit_cost)
            total_input_cost += row.total_cost

        for row in self.activity_worker:
            total_labour_cost += flt(row.wages)

        self.total_input_cost = total_input_cost
        self.total_labour_cost = total_labour_cost

        self.total_activity_cost = (
            total_input_cost + total_labour_cost
        )