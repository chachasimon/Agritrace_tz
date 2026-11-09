# Copyright (c) 2026, aakvatech limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Crop(Document):

    def validate(self):
        self.validate_crop_name()
        self.validate_default_unit()
        self.validate_item()

    def validate_crop_name(self):
        if not self.crop_name or not self.crop_name.strip():
            frappe.throw("Crop Name is required.")

        self.crop_name = self.crop_name.strip()

        existing_crop = frappe.get_all(
            "Crop",
            filters={
                "name": ["!=", self.name]
            },
            fields=["crop_name"]
        )

        for crop in existing_crop:
            if crop.crop_name.strip().lower() == self.crop_name.lower():
                frappe.throw(
                    f"Crop '{self.crop_name}' already exists."
                )

    def validate_default_unit(self):
        if not frappe.db.exists("UOM", self.default_unit):
            frappe.throw("Please select a valid Default Unit.")

    def validate_item(self):
        if not self.custom_item:
            return

        item = frappe.db.get_value(
            "Item",
            self.custom_item,
            ["stock_uom", "is_stock_item"],
            as_dict=True
        )

        if not item:
            frappe.throw("Selected Item does not exist.")

        if not item.is_stock_item:
            frappe.throw(
                "Selected Item must be a Stock Item."
            )

        if item.stock_uom != self.default_unit:
            frappe.throw(
                f"Item Stock UOM ({item.stock_uom}) must match "
                f"Crop Default Unit ({self.default_unit})."
            )