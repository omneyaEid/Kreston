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
        # Convert grey_area_names to list if it's passed as a JSON string
        if isinstance(grey_area_names, str):
            grey_area_names = json.loads(grey_area_names)

        # Check if the current date allows moving to Lead
        move_to_lead = frappe.db.get_single_value("Global Settings", "move_to_lead")
        if move_to_lead != getdate():
            frappe.throw(f"Could not move to Lead, only allowed on {move_to_lead}")

        # Fetch Lead doctype metadata
        lead_meta = frappe.get_meta("Lead")
        lead_fields = {field.fieldname for field in lead_meta.fields}

        for grey_area_name in grey_area_names:
            # Fetch the Grey Area document
            grey_area_doc = frappe.get_doc("Grey Area", grey_area_name)
            
            # Fetch the archived Lead doc linked to this Grey Area
            archived_lead_doc = frappe.get_doc("Lead", {"custom_grey_area": grey_area_name})

            archived_lead_doc.custom_grey_area = None
            archived_lead_doc.save(ignore_permissions=True)

            # Create a new Lead document
            new_lead_doc = frappe.new_doc("Lead")

            # Copy relevant fields from Grey Area to the new Lead
            for fieldname in lead_fields:
                if fieldname in lead_fields:
                    new_lead_doc.set(fieldname, archived_lead_doc.get(fieldname))

            # Insert the new Lead document
            new_lead_doc.custom_archive = 0
            new_lead_doc.custom_grey_area = None 

            new_lead_doc.flags.ignore_validate = True
            new_lead_doc.insert(ignore_permissions=True, ignore_mandatory=True)
            

            # Update linked services from Grey Area to new Lead
            for service in services:
                # Fetch all service records linked to the grey_area_name
                service_docs = frappe.get_all(
                    service,
                    filters={"linked_service": grey_area_name},
                    fields=["name", "linked_service"]
                )

                # Update each service to link to the new Lead
                for service_doc in service_docs:
                    service_record = frappe.get_doc(service, service_doc["name"])
                    service_record.linked_service = new_lead_doc.name
                    service_record.linked_doctype = "Lead"
                    service_record.save(ignore_permissions=True)

            # Optionally delete the Grey Area document after moving the services
            grey_area_doc.delete(ignore_permissions=True)

        return {"message": "Grey Area documents moved to Lead and services updated successfully."}

    except Exception as e:
        frappe.throw(str(e))
