app_name = "agritrace_tz"
app_title = "Agritrace Tz"
app_publisher = "aakvatech limited"
app_description = "agritrace it is the system for farmers management"
app_email = "ngainachacha@gmail.com"
app_license = "mit"


permission_query_conditions = {
    "Farmer": "agritrace_tz.agritrace_tz.permission.get_farmer_query",
    "Farm": "agritrace_tz.agritrace_tz.permission.get_farm_query",
    "Farm Plot": "agritrace_tz.agritrace_tz.permission.get_farm_plot_query",
    "Agricultural Season": "agritrace_tz.agritrace_tz.permission.get_agricultural_season_query",
    "Crop Cycle": "agritrace_tz.agritrace_tz.permission.get_crop_cycle_query",
    "Agricultural Activity": "agritrace_tz.agritrace_tz.permission.get_agricultural_activity_query",
    "Farm Worker": "agritrace_tz.agritrace_tz.permission.get_farm_worker_query",
    "Farm Worker Payment": "agritrace_tz.agritrace_tz.permission.get_farm_worker_payment_query",
    "Farm Budget": "agritrace_tz.agritrace_tz.permission.get_farm_budget_query",
    "Farm Expense": "agritrace_tz.agritrace_tz.permission.get_farm_expense_query",
    "Farm Income": "agritrace_tz.agritrace_tz.permission.get_farm_income_query",
    "Harvest Record": "agritrace_tz.agritrace_tz.permission.get_harvest_record_query",
    "Soil Test": "agritrace_tz.agritrace_tz.permission.get_soil_test_query",
    "Irrigation Records": "agritrace_tz.agritrace_tz.permission.get_irrigation_records_query",
    "Work Record": "agritrace_tz.agritrace_tz.permission.get_work_record_query",
    "Produce Loss Record": "agritrace_tz.agritrace_tz.permission.get_produce_loss_record_query",
    "Produce Quality Inspection": "agritrace_tz.agritrace_tz.permission.get_produce_quality_inspection_query",
    "Paste And Disease Observation": "agritrace_tz.agritrace_tz.permission.get_paste_and_disease_observation_query",
    "Farm Equipment Usage": "agritrace_tz.agritrace_tz.permission.get_farm_equipment_usage_query",
    "Farm Worker Assignment": "agritrace_tz.agritrace_tz.permission.get_farm_worker_assignment_query",
    "Farm Activity": "agritrace_tz.agritrace_tz.permission.get_farm_activity_query",
    "Crop": "agritrace_tz.agritrace_tz.permission.get_crop_query",
    "Farm Activity Type": "agritrace_tz.agritrace_tz.permission.get_farm_activity_type_query",
    "Warehouse": "agritrace_tz.agritrace_tz.permission.get_warehouse_query",
    "Asset": "agritrace_tz.agritrace_tz.permission.get_asset_query",
    "Asset Repair": "agritrace_tz.agritrace_tz.permission.get_asset_repair_query",
    "Asset Maintenance": "agritrace_tz.agritrace_tz.permission.get_asset_maintenance_query",
    "Asset Maintenance Log": "agritrace_tz.agritrace_tz.permission.get_asset_maintenance_log_query",
    "Material Request": "agritrace_tz.agritrace_tz.permission.get_material_request_query",
    "Purchase Order": "agritrace_tz.agritrace_tz.permission.get_purchase_order_query",
    "Purchase Receipt": "agritrace_tz.agritrace_tz.permission.get_purchase_receipt_query",
    "Purchase Invoice": "agritrace_tz.agritrace_tz.permission.get_purchase_invoice_query",
    "Stock Entry": "agritrace_tz.agritrace_tz.permission.get_stock_entry_query",
    "Sales Order": "agritrace_tz.agritrace_tz.permission.get_sales_order_query",
    "Sales Invoice": "agritrace_tz.agritrace_tz.permission.get_sales_invoice_query",
    "Supplier": "agritrace_tz.agritrace_tz.permission.get_supplier_query",
    "Customer": "agritrace_tz.agritrace_tz.permission.get_customer_query",
}


has_permission = {
    "Farmer": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Farm": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Farm Plot": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Agricultural Season": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Crop Cycle": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Agricultural Activity": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Farm Worker": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Farm Worker Payment": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Farm Budget": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Farm Expense": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Farm Income": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Harvest Record": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Soil Test": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Irrigation Records": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Work Record": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Produce Loss Record": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Produce Quality Inspection": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Paste And Disease Observation": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Farm Equipment Usage": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Farm Worker Assignment": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Farm Activity": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Crop": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Farm Activity Type": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Warehouse": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Asset": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Asset Repair": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Asset Maintenance": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Asset Maintenance Log": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Material Request": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Purchase Order": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Purchase Receipt": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Purchase Invoice": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Stock Entry": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Sales Order": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Sales Invoice": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Supplier": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
    "Customer": "agritrace_tz.agritrace_tz.permission.has_farmer_permission",
}


doc_events = {
    # Farm management
    "Farm": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Farm Plot": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Agricultural Season": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Crop Cycle": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Agricultural Activity": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Farm Worker": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Farm Worker Payment": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Farm Budget": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Farm Expense": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Farm Income": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Harvest Record": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Soil Test": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Irrigation Records": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Work Record": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Produce Loss Record": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Produce Quality Inspection": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Paste And Disease Observation": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Farm Equipment Usage": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },
    "Farm Worker Assignment": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership"
    },

    # ERPNext ownership validation + existing custom validation
    "Warehouse": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership",
        "validate": "agritrace_tz.agritrace_tz.warehouse.validate_warehouse"
    },
    "Asset": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership",
        "validate": "agritrace_tz.agritrace_tz.asset.validate_asset"
    },
    "Asset Repair": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership",
        "validate": "agritrace_tz.agritrace_tz.asset_repair.validate_asset_repair"
    },
    "Asset Maintenance": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership",
        "validate": "agritrace_tz.agritrace_tz.asset_maintenance.validate_asset_maintenance"
    },
    "Asset Maintenance Log": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership",
        "validate": "agritrace_tz.agritrace_tz.asset_maintenance_log.validate_asset_maintenance_log"
    },
    "Material Request": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership",
        "validate": "agritrace_tz.agritrace_tz.material_request.validate_material_request"
    },
    "Purchase Order": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership",
        "validate": "agritrace_tz.agritrace_tz.purchase_order.validate_purchase_order"
    },
    "Purchase Receipt": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership",
        "validate": "agritrace_tz.agritrace_tz.purchase_receipt.validate_purchase_receipt"
    },
    "Stock Entry": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership",
        "validate": "agritrace_tz.agritrace_tz.stock_entry.validate_stock_entry"
    },
    "Purchase Invoice": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership",
        "validate": "agritrace_tz.agritrace_tz.purchase_invoice.validate_purchase_invoice"
    },
    "Sales Order": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership",
        "validate": "agritrace_tz.agritrace_tz.sales_order.validate_sales_order"
    },
    "Sales Invoice": {
        "before_validate": "agritrace_tz.agritrace_tz.permission.validate_document_ownership",
        "validate": "agritrace_tz.agritrace_tz.sales_invoice.validate_sales_invoice"
    },

    # Supplier and Customer keep their dedicated ownership validation
    "Supplier": {
        "before_validate": "agritrace_tz.agritrace_tz.party.validate_party_ownership"
    },
    "Customer": {
        "before_validate": "agritrace_tz.agritrace_tz.party.validate_party_ownership"
    }
}

scheduler_events = {
    "hourly": [
        "agritrace_tz.tasks.check_farm_budget_alerts"
    ],
    "daily": [
        "agritrace_tz.tasks.check_worker_payment_reminders"
    ]
}
# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "agritrace_tz",
# 		"logo": "/assets/agritrace_tz/logo.png",
# 		"title": "Agritrace Tz",
# 		"route": "/agritrace_tz",
# 		"has_permission": "agritrace_tz.api.permission.has_app_permission",
# 	}
# ]

# The dock, the rail down the left of the desk, is a document rather than a hook. Author it in
# Manage Dock on a developer-mode site and press Export to App, and it is written to
# `agritrace_tz/dock/agritrace_tz/agritrace_tz.json` for git to carry. An app that ships none has no
# rail: its sidebar gets a switcher in the header instead.
#
# A companion app, one that extends a host app rather than standing on its own, says so with
# `mount_on` on that same record, and its entries are appended to the host's rail. Mounting keeps
# the companion off the apps screen, so it takes precedence over any add_to_apps_screen above.

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/agritrace_tz/css/agritrace_tz.css"
# app_include_js = "/assets/agritrace_tz/js/agritrace_tz.js"

# include js, css files in header of web template
# web_include_css = "/assets/agritrace_tz/css/agritrace_tz.css"
# web_include_js = "/assets/agritrace_tz/js/agritrace_tz.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "agritrace_tz/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_kanban_js = {"doctype" : "public/js/doctype_kanban.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "agritrace_tz/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "agritrace_tz.utils.jinja_methods",
# 	"filters": "agritrace_tz.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "agritrace_tz.install.before_install"
# after_install = "agritrace_tz.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "agritrace_tz.uninstall.before_uninstall"
# after_uninstall = "agritrace_tz.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "agritrace_tz.utils.before_app_install"
# after_app_install = "agritrace_tz.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "agritrace_tz.utils.before_app_uninstall"
# after_app_uninstall = "agritrace_tz.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "agritrace_tz.build.after_build"

# To hook into the build process of other apps
# The list of apps being built is passed as an argument

# after_app_build = "agritrace_tz.build.after_app_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "agritrace_tz.notifications.get_notification_config"

# Awesome Bar
# -----------
# Extra search results: list of dicts with label, description, route, index.
# route: ["List", "ToDo"], "/desk/docs/some/page", or "https://example.com"
# awesomebar_search = ["agritrace_tz.search.awesomebar_results"]

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"agritrace_tz.tasks.all"
# 	],
# 	"daily": [
# 		"agritrace_tz.tasks.daily"
# 	],
# 	"hourly": [
# 		"agritrace_tz.tasks.hourly"
# 	],
# 	"weekly": [
# 		"agritrace_tz.tasks.weekly"
# 	],
# 	"monthly": [
# 		"agritrace_tz.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "agritrace_tz.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "agritrace_tz.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "agritrace_tz.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "agritrace_tz.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["agritrace_tz.utils.before_request"]
# after_request = ["agritrace_tz.utils.after_request"]

# Job Events
# ----------
# before_job = ["agritrace_tz.utils.before_job"]
# after_job = ["agritrace_tz.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"agritrace_tz.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []
