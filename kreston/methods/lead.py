import frappe
import json
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
def calc_lead_totals(doctype, name):
    total_audit_budget = 0.0  # Initialize as float
    total_audit_expenses = 0.0  # Initialize as float
    audit_write_up_down = 0.0  # Initialize as float

    for service in services:
        records = frappe.get_all(
            service,
            filters=[
                ["linked_doctype", "=", doctype],
                ["linked_service", "=", name],
            ],
            fields=[
                "total_audit_budget",
                "total_audit_expenses",
                "audit_write_up_down",
            ],
            limit=1,
            order_by="creation DESC",
        )

        # Loop through the records (even though we limit to 1, it's good practice)
        for record in records:
            # Safely convert to float or use 0 if it's not a valid float
            total_audit_budget += float(record.get("total_audit_budget", 0) or 0)
            total_audit_expenses += float(record.get("total_audit_expenses", 0) or 0)
            audit_write_up_down += float(record.get("audit_write_up_down", 0) or 0)

    return {
        "total_audit_budget": total_audit_budget,
        "total_audit_expenses": total_audit_expenses,
        "audit_write_up_down": audit_write_up_down,
    }





@frappe.whitelist()
def move_to_grey_area(lead_names):
    try:
        if isinstance(lead_names, str):
            lead_names = json.loads(lead_names)

        move_to_grey_area = frappe.db.get_single_value("Global Settings", "move_to_grey_area")
        if move_to_grey_area != getdate() :
            frappe.throw(f"Could not Move to grey area, only allow in  {move_to_grey_area}")


        # Get the meta data for the Grey Area doctype
        grey_area_meta = frappe.get_meta("Grey Area")
        grey_area_fields = {field.fieldname for field in grey_area_meta.fields}

        for lead_name in lead_names:
            lead_doc = frappe.get_doc("Lead", lead_name)
            if lead_doc.custom_pipeline_status in [ "Win","Lost Fit"]:
                # Create a new Grey Area document
                grey_area_doc = frappe.new_doc("Grey Area")

                # Get the meta for Lead doctype
                lead_meta = frappe.get_meta("Lead")
                lead_fields = {field.fieldname for field in lead_meta.fields}

                # Copy fields from Lead to Grey Area
                for fieldname in lead_fields:
                    if fieldname in grey_area_fields:  # Check if the field exists in the Grey Area doctype
                        grey_area_doc.set(fieldname, lead_doc.get(fieldname))

                # Insert the new Grey Area document
                grey_area_doc.insert(ignore_permissions=True,ignore_mandatory=True)

                # Loop through the services and check if linked_service matches the lead_name
                for service in services:
                    # Try to fetch the service record where linked_service matches the lead_name
                    service_docs = frappe.get_all(service, filters={"linked_service": lead_name}, fields=["name", "linked_service"])

                    for service_doc in service_docs:
                        # If the linked_service matches lead_name, update it
                        if service_doc.get("linked_service") == lead_name:
                            # Update the service document to reference the new Grey Area document name
                            service_record = frappe.get_doc(service, service_doc["name"])
                            service_record.linked_service = grey_area_doc.name
                            service_record.linked_doctype = "Grey Area"  # Ensure the linked_doctype is updated
                            service_record.save(ignore_permissions=True)

                # Optionally, delete the lead after updating the linked services
                lead_doc.delete(ignore_permissions=True)

        return {"message": "Leads moved to Grey Area and services updated successfully."}
    
    except Exception as e:
        frappe.throw(str(e))
