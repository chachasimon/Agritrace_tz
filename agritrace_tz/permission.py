def has_farmer_permission(doc, user=None, ptype=None):
    user = user or frappe.session.user
    ptype = ptype or "read"

    if is_privileged_user(user):
        return True

    if not user or user == "Guest":
        return False

    roles = frappe.get_roles(user)

    if "Farmer" not in roles:
        return None

    # Shared reference data is read-only.
    if doc.doctype in SHARED_READ_ONLY_DOCTYPES:
        return ptype == "read"

    # Farmer master is read-only and restricted to its owner.
    if doc.doctype == "Farmer":
        return (
            ptype == "read"
            and doc.user_account == user
        )

    if ptype not in FARMER_ALLOWED_PERMISSIONS:
        return False

    farmer = get_linked_farmer(user)

    if not farmer:
        return False

    # Allow controller permission check for new owned documents.
    # Standard Role Permissions still control actual access.
    if doc.is_new():
        farmer_field, farm_field = get_ownership_fields(doc.doctype)

        if farmer_field or farm_field:
            return ptype == "create"

        return False

    return get_document_farmer(doc) == farmer
