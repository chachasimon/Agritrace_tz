import frappe

from agritrace_tz.agritrace_tz.permission import (
    get_linked_farmer,
    is_privileged_user,
)


def validate_party_ownership(doc, method=None):
    """
    Enforce Farmer ownership for Supplier and Customer.

    - Automatically assign the logged-in Farmer on new records.
    - Prevent Farmers from assigning records to another Farmer.
    - Prevent Farmers from changing ownership of existing records.
    - Preserve full access for privileged users.
    """

    user = frappe.session.user

    # Privileged users can manage all Supplier and Customer records.
    if is_privileged_user(user):
        return

    # Other non-Farmer roles use standard ERPNext permissions.
    if "Farmer" not in frappe.get_roles(user):
        return

    farmer = get_linked_farmer(user)

    if not farmer:
        frappe.throw(
            "Your user account is not linked to a Farmer record."
        )

    # Automatically assign ownership to the logged-in Farmer.
    if not doc.custom_farmer:
        doc.custom_farmer = farmer

    # Prevent ownership assignment or transfer to another Farmer.
    if doc.custom_farmer != farmer:
        frappe.throw(
            "You can only create or manage Supplier and Customer "
            "records belonging to your own Farmer account."
        )
