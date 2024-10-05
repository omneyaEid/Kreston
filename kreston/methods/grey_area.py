import json

import frappe
from frappe.utils import getdate

services = [
    "Audit Service",
    "Audit SP Service",
    "Z Cases Service",
    "ZDP SP Service",
    "VAT Service",
    "VAT Cases Service",
    "AUP Service",
    "LC Service",
    "Zakat Service",
    "Tax Service",
    "SOM Service",
    "VDP SP Service",
]


@frappe.whitelist()
def move_from_grey_area(grey_area_names):
    try:
        if isinstance(grey_area_names, str):
            grey_area_names = json.loads(grey_area_names)

        move_to_lead = frappe.db.get_single_value("Global Settings", "move_to_lead")
        if move_to_lead != getdate():
            frappe.throw(f"Could not move to Lead, only allowed on {move_to_lead}")

        # Get the meta data for the Lead doctype
        lead_meta = frappe.get_meta("Lead")
        lead_fields = {field.fieldname for field in lead_meta.fields}

        for grey_area_name in grey_area_names:
            grey_area_doc = frappe.get_doc("Grey Area", grey_area_name)
            if True:
            # if grey_area_doc.custom_pipeline_status in [
            #     "Prospect",
            #     "Proposal",
            #     "Engagement Letter",
            #     "Win",
            #     "Lost Fit",
            #     "Lost Not Fit",
            # ]:

                # Create a new Lead document
                lead_doc = frappe.new_doc("Lead")

                # Get the meta for Grey Area doctype
                grey_area_meta = frappe.get_meta("Grey Area")
                grey_area_fields = {field.fieldname for field in grey_area_meta.fields}

                # Copy fields from Grey Area to Lead
                for fieldname in grey_area_fields:
                    if (
                        fieldname in lead_fields
                    ):  # Check if the field exists in the Lead doctype
                        lead_doc.set(fieldname, grey_area_doc.get(fieldname))

                # Insert the new Lead document
                lead_doc.insert(ignore_permissions=True,ignore_mandatory=True)

                for service in services:
                    # Try to fetch the service record where linked_service matches the grey_area_name
                    service_docs = frappe.get_all(
                        service,
                        filters={"linked_service": grey_area_name},
                        fields=["name", "linked_service"],
                    )

                    for service_doc in service_docs:
                        # If the linked_service matches grey_area_name, update it
                        if service_doc.get("linked_service") == grey_area_name:
                            # Update the service document to reference the new Lead document name
                            service_record = frappe.get_doc(
                                service, service_doc["name"]
                            )
                            service_record.linked_service = lead_doc.name
                            service_record.linked_doctype = (
                                "Lead"  # Ensure the linked_doctype is updated
                            )
                            service_record.save(ignore_permissions=True)

                # Optionally, delete the Grey Area document after updating the linked services
                grey_area_doc.delete(ignore_permissions=True)

        return {
            "message": "Grey Area documents moved to Lead and services updated successfully."
        }

    except Exception as e:
        frappe.throw(str(e))
