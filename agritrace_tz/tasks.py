import frappe
from frappe.utils import flt


def check_farm_budget_alerts():
    """Check active farm budgets and notify farmers at 80% and 100% usage."""

    budgets = frappe.get_all(
        "Farm Budget",
        filters={"status": "Active"},
        fields=[
            "name",
            "budget_name",
            "farmer",
            "farm",
            "budget_start_date",
            "budget_end_date",
            "total_planned_expense"
        ]
    )

    for budget in budgets:

        planned_expense = flt(budget.total_planned_expense)

        if planned_expense <= 0:
            continue

        if not budget.farmer or not budget.farm:
            continue

        if not budget.budget_start_date or not budget.budget_end_date:
            continue

        farmer = frappe.db.get_value(
            "Farmer",
            budget.farmer,
            ["user_account", "status"],
            as_dict=True
        )

        if not farmer or farmer.status != "Active":
            continue

        if not farmer.user_account:
            continue

        user_enabled = frappe.db.get_value(
            "User",
            farmer.user_account,
            "enabled"
        )

        if not user_enabled:
            continue

        expenses = frappe.get_all(
            "Farm Expense",
            filters={
                "farmer": budget.farmer,
                "farm": budget.farm,
                "expense_date": [
                    "between",
                    [budget.budget_start_date, budget.budget_end_date]
                ]
            },
            fields=["amount"]
        )

        total_expense = sum(
            flt(row.amount) for row in expenses
        )

        usage_percentage = (
            total_expense / planned_expense
        ) * 100

        thresholds = [80, 100]

        for threshold in thresholds:

            if usage_percentage < threshold:
                continue

            subject = (
                f"Farm Budget Alert: {budget.name} - {threshold}%"
            )

            already_sent = frappe.db.exists(
                "Notification Log",
                {
                    "document_type": "Farm Budget",
                    "document_name": budget.name,
                    "for_user": farmer.user_account,
                    "subject": subject
                }
            )

            if already_sent:
                continue

            message = (
                f"Your farm budget '{budget.budget_name}' "
                f"has reached {usage_percentage:.1f}% usage. "
                f"Total expenses: TZS {total_expense:,.2f}. "
                f"Planned expenses: TZS {planned_expense:,.2f}."
            )

            frappe.get_doc({
                "doctype": "Notification Log",
                "type": "Alert",
                "title": "Farm Budget Alert",
                "subject": subject,
                "email_content": message,
                "description": message,
                "for_user": farmer.user_account,
                "document_type": "Farm Budget",
                "document_name": budget.name
            }).insert(ignore_permissions=True)

            frappe.logger("agritrace_budget").info(
                f"Budget alert sent: {budget.name}, "
                f"threshold: {threshold}%, "
                f"usage: {usage_percentage:.1f}%"
            )


def check_worker_payment_reminders():
    """Send daily reminders for overdue unpaid or partially paid worker payments."""

    today = frappe.utils.getdate()

    payments = frappe.get_all(
        "Farm Worker Payment",
        filters={
            "payment_status": ["in", ["Unpaid", "Partially Paid"]],
            "balance": [">", 0],
            "payment_period_end": ["<=", today]
        },
        fields=[
            "name",
            "farmer",
            "worker",
            "farm",
            "payment_period_end",
            "amount_due",
            "amount_paid",
            "balance",
            "payment_status"
        ]
    )

    for payment in payments:

        if not payment.farmer:
            continue

        farmer = frappe.db.get_value(
            "Farmer",
            payment.farmer,
            ["user_account", "status"],
            as_dict=True
        )

        if not farmer or farmer.status != "Active":
            continue

        if not farmer.user_account:
            continue

        user_enabled = frappe.db.get_value(
            "User",
            farmer.user_account,
            "enabled"
        )

        if not user_enabled:
            continue

        subject = (
            f"Worker Payment Reminder: "
            f"{payment.name} - {today}"
        )

        already_sent_today = frappe.db.exists(
            "Notification Log",
            {
                "document_type": "Farm Worker Payment",
                "document_name": payment.name,
                "for_user": farmer.user_account,
                "subject": subject
            }
        )

        if already_sent_today:
            continue

        message = (
            f"Your worker payment for {payment.worker} is overdue. "
            f"Payment period ended on {payment.payment_period_end}. "
            f"Amount due: TZS {payment.amount_due:,.2f}. "
            f"Amount paid: TZS {payment.amount_paid:,.2f}. "
            f"Outstanding balance: TZS {payment.balance:,.2f}. "
            f"Please complete the outstanding payment."
        )

        frappe.get_doc({
            "doctype": "Notification Log",
            "type": "Alert",
            "title": "Worker Payment Reminder",
            "subject": subject,
            "description": message,
            "email_content": message,
            "for_user": farmer.user_account,
            "document_type": "Farm Worker Payment",
            "document_name": payment.name
        }).insert(ignore_permissions=True)

        frappe.logger("agritrace_worker_payment").info(
            f"Daily reminder created for {payment.name}"
        )