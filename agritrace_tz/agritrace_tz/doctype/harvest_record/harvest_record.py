# Copyright (c) 2026, aakvatech limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate, today


class HarvestRecord(Document):

    def validate(self):
        self.validate_farmer()
        self.validate_farm()
        self.validate_crop_cycle()
        self.validate_plot()
        self.validate_harvest_date()
        self.validate_harvested_by()
        self.validate_uom()
        self.validate_harvest_details()
        self.calculate_total_quantity()

    # --------------------------------------------------
    # FARMER VALIDATION
    # --------------------------------------------------

    def validate_farmer(self):

        if not self.farmer:
            frappe.throw(_("Please select a Farmer."))

        if not frappe.db.exists("Farmer", self.farmer):
            frappe.throw(_("Selected Farmer does not exist."))

    # --------------------------------------------------
    # FARM VALIDATION
    # --------------------------------------------------

    def validate_farm(self):

        if not self.farm:
            frappe.throw(_("Please select a Farm."))

        farm_farmer = frappe.db.get_value(
            "Farm",
            self.farm,
            "farmer"
        )

        if farm_farmer != self.farmer:
            frappe.throw(
                _("Selected Farm does not belong to the selected Farmer.")
            )

    # --------------------------------------------------
    # CROP CYCLE VALIDATION
    # --------------------------------------------------

    def validate_crop_cycle(self):

        if not self.crop_cycle:
            frappe.throw(_("Please select a Crop Cycle."))

        cycle = frappe.db.get_value(
            "Crop Cycle",
            self.crop_cycle,
            ["farmer", "farm", "plot", "planting_date"],
            as_dict=True
        )

        if not cycle:
            frappe.throw(_("Selected Crop Cycle does not exist."))

        if cycle.farmer != self.farmer:
            frappe.throw(
                _("Selected Crop Cycle belongs to another Farmer.")
            )

        if cycle.farm != self.farm:
            frappe.throw(
                _("Selected Crop Cycle belongs to another Farm.")
            )

        if cycle.plot != self.plot:
            frappe.throw(
                _("Selected Crop Cycle belongs to another Plot.")
            )

    # --------------------------------------------------
    # PLOT VALIDATION
    # --------------------------------------------------

    def validate_plot(self):

        if not self.plot:
            frappe.throw(_("Please select a Plot."))

        plot_farm = frappe.db.get_value(
            "Farm Plot",
            self.plot,
            "farm"
        )

        if plot_farm != self.farm:
            frappe.throw(
                _("Selected Plot does not belong to the selected Farm.")
            )

    # --------------------------------------------------
    # HARVEST DATE VALIDATION
    # --------------------------------------------------

    def validate_harvest_date(self):

        if not self.harvest_date:
            frappe.throw(_("Please select a Harvest Date."))

        harvest_date = getdate(self.harvest_date)

        if harvest_date > getdate(today()):
            frappe.throw(_("Harvest Date cannot be in the future."))

        planting_date = frappe.db.get_value(
            "Crop Cycle",
            self.crop_cycle,
            "planting_date"
        )

        if planting_date and harvest_date < getdate(planting_date):
            frappe.throw(
                _("Harvest Date cannot be before the Planting Date.")
            )

    # --------------------------------------------------
    # WORKER VALIDATION
    # --------------------------------------------------

    def validate_harvested_by(self):

        if self.harvested_by:

            worker_farmer = frappe.db.get_value(
                "Farm Worker",
                self.harvested_by,
                "farmer"
            )

            if worker_farmer != self.farmer:
                frappe.throw(
                    _("Selected Worker does not belong to the selected Farmer.")
                )

    # --------------------------------------------------
    # UOM VALIDATION
    # --------------------------------------------------

    def validate_uom(self):

        if not self.uom:
            frappe.throw(
                _("Please select a standard UOM for this harvest.")
            )

        for row in self.harvest_detail:

            if not row.uom:
                frappe.throw(
                    _("Please select a UOM for every Harvest Detail row.")
                )

            if row.uom != self.uom:
                frappe.throw(
                    _("UOM mismatch in Harvest Detail. "
                      "All rows must use {0}.").format(self.uom)
                )

    # --------------------------------------------------
    # HARVEST DETAILS VALIDATION
    # --------------------------------------------------

    def validate_harvest_details(self):

        if not self.harvest_detail:
            frappe.throw(
                _("Please add at least one Harvest Detail row.")
            )

        for row in self.harvest_detail:

            if flt(row.quantity) <= 0:
                frappe.throw(
                    _("Harvest quantity must be greater than zero.")
                )

            if not row.uom:
                frappe.throw(
                    _("Please select a UOM for every Harvest Detail row.")
                )

    # --------------------------------------------------
    # TOTAL HARVEST QUANTITY
    # --------------------------------------------------

    def calculate_total_quantity(self):

        self.total_quantity = sum(
            flt(row.quantity)
            for row in self.harvest_detail
        )

    # ==================================================
    # HARVEST TO ERPNext STOCK ENTRY INTEGRATION
    # ==================================================

    @frappe.whitelist()
    def create_stock_entry(self):

        # Ensure Harvest Record is saved
        if not self.name:
            frappe.throw(
                _("Please save the Harvest Record first.")
            )

        # Check permission
        self.check_permission("write")

        # Reload latest saved document
        self.reload()

        # Prevent duplicate Stock Entry
        if self.stock_entry:
            frappe.throw(
                _("Stock Entry {0} has already been created "
                  "for this Harvest Record.").format(self.stock_entry)
            )

        # Re-run Harvest Record validations
        self.validate()

        # Calculate total quantity from all grades
        total_quantity = sum(
            flt(row.quantity)
            for row in self.harvest_detail
        )

        if total_quantity <= 0:
            frappe.throw(
                _("Total Harvest Quantity must be greater than zero.")
            )

        # Get Crop from Crop Cycle
        crop = frappe.db.get_value(
            "Crop Cycle",
            self.crop_cycle,
            "crop"
        )

        if not crop:
            frappe.throw(
                _("Could not identify the Crop from Crop Cycle.")
            )

        # Get ERPNext Item linked to Crop
        item_code = frappe.db.get_value(
            "Crop",
            crop,
            "custom_item"
        )

        if not item_code:
            frappe.throw(
                _("Please link an ERPNext Stock Item to Crop {0}.")
                .format(crop)
            )

        # Validate Item
        item = frappe.db.get_value(
            "Item",
            item_code,
            ["stock_uom", "is_stock_item"],
            as_dict=True
        )

        if not item or not item.is_stock_item:
            frappe.throw(
                _("Selected Crop Item must be a Stock Item.")
            )

        # Validate UOM
        if item.stock_uom != self.uom:
            frappe.throw(
                _("Harvest UOM must match Item Stock UOM ({0}).")
                .format(item.stock_uom)
            )

        # Get produce warehouse
        warehouse_name = "Agritrace Produce Warehouse - AL"

        warehouse = frappe.db.get_value(
            "Warehouse",
            warehouse_name,
            [
                "company",
                "is_group",
                "custom_farmer",
                "custom_farm",
                "custom_is_agritrace_warehouse"
            ],
            as_dict=True
        )

        if not warehouse:
            frappe.throw(
                _("AgriTrace Produce Warehouse does not exist.")
            )

        # Validate warehouse ownership
        if not warehouse.custom_is_agritrace_warehouse:
            frappe.throw(
                _("Selected Warehouse is not an AgriTrace Warehouse.")
            )

        if warehouse.custom_farmer != self.farmer:
            frappe.throw(
                _("Produce Warehouse does not belong to this Farmer.")
            )

        if warehouse.custom_farm != self.farm:
            frappe.throw(
                _("Produce Warehouse does not belong to this Farm.")
            )

        if warehouse.is_group:
            frappe.throw(
                _("Please select a non-group Warehouse.")
            )

        # Validate Material Receipt type
        if not frappe.db.exists(
            "Stock Entry Type",
            "Material Receipt"
        ):
            frappe.throw(
                _("Material Receipt Stock Entry Type does not exist.")
            )

        # Create Stock Entry document
        stock_entry = frappe.new_doc("Stock Entry")

        stock_entry.stock_entry_type = "Material Receipt"
        stock_entry.purpose = "Material Receipt"

        stock_entry.company = warehouse.company

        stock_entry.custom_farmer = self.farmer
        stock_entry.custom_farm = self.farm

        stock_entry.posting_date = self.harvest_date

        # Add one item line containing total harvest quantity
        stock_entry.append(
            "items",
            {
                "item_code": item_code,
                "qty": total_quantity,
                "uom": self.uom,
                "stock_uom": item.stock_uom,
                "conversion_factor": 1,
                "t_warehouse": warehouse_name
            }
        )

        # Save as Draft
        stock_entry.insert()

        # Link Stock Entry to Harvest Record
        self.db_set(
            "stock_entry",
            stock_entry.name
        )

        return {
            "stock_entry": stock_entry.name,
            "status": stock_entry.docstatus,
            "total_quantity": total_quantity,
            "item_code": item_code
        }