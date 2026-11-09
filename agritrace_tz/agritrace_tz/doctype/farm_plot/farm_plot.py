# Copyright (c) 2026, aakvatech limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FarmPlot(Document):

    def validate(self):
        self.validate_farm()
        self.validate_plot_size()
        self.validate_total_plot_area()

    def validate_farm(self):
        if not frappe.db.exists("Farm", self.farm):
            frappe.throw("The selected Farm does not exist.")

        farm_status = frappe.db.get_value(
            "Farm",
            self.farm,
            "status"
        )

        if farm_status != "Active":
            frappe.throw("You can only register plots under an active Farm.")

    def validate_plot_size(self):
        if self.plot_size is None or self.plot_size <= 0:
            frappe.throw("Plot size must be greater than zero.")

    def validate_total_plot_area(self):
        farm = frappe.get_doc("Farm", self.farm)

        # Convert all measurements to square metres.
        unit_conversion = {
            "Acre": 4046.8564224,
            "Hectare": 10000
        }

        farm_unit = farm.area_unit
        plot_unit = self.area_unit

        if farm_unit not in unit_conversion or plot_unit not in unit_conversion:
            frappe.throw("Please select a valid area unit for the Farm and Plot.")

        farm_area = (farm.total_size or 0) * unit_conversion[farm_unit]

        existing_plots = frappe.get_all(
            "Farm Plot",
            filters={
                "farm": self.farm,
                "name": ["!=", self.name]
            },
            fields=["plot_size", "area_unit"]
        )

        allocated_area = 0

        for plot in existing_plots:
            allocated_area += (
                plot.plot_size * unit_conversion[plot.area_unit]
            )

        current_plot_area = self.plot_size * unit_conversion[plot_unit]

        total_allocated_area = allocated_area + current_plot_area

        if total_allocated_area > farm_area:
            frappe.throw(
                "The total size of plots cannot exceed the total size of the Farm."
            )