import frappe
from frappe import throw, _
import json
from frappe.utils import getdate, add_to_date

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
        if move_to_grey_area != getdate():
            frappe.throw(f"Could not move to grey area, only allowed on {move_to_grey_area}")

        # Get the meta data for the Grey Area doctype
        grey_area_meta = frappe.get_meta("Grey Area")
        grey_area_fields = {field.fieldname for field in grey_area_meta.fields}

        for lead_name in lead_names:
            lead_doc = frappe.get_doc("Lead", lead_name)
            if lead_doc.custom_pipeline_status in ["Win", "Lost Fit"]:
                # Create a new Grey Area document
                grey_area_doc = frappe.new_doc("Grey Area")

                # Get the meta for Lead doctype
                lead_meta = frappe.get_meta("Lead")
                lead_fields = {field.fieldname for field in lead_meta.fields}

                # Copy fields from Lead to Grey Area
                for fieldname in lead_fields:
                    if fieldname in grey_area_fields:  # Check if the field exists in the Grey Area doctype
                        grey_area_doc.set(fieldname, lead_doc.get(fieldname))
                
                grey_area_doc.lead = lead_name

                # Insert the new Grey Area document
                grey_area_doc.insert(ignore_permissions=True, ignore_mandatory=True)

                # Loop through the services and check if linked_service matches the lead_name
                for service in services:
                    # Fetch the service records where linked_service matches the lead_name
                    service_docs = frappe.get_all(service, filters={"linked_service": lead_name}, fields=["name", "linked_service"])

                    for service_doc in service_docs:
                        # Get the service record
                        service_record = frappe.get_doc(service, service_doc["name"])

                        # Create a copy of the service record
                        new_service_doc = frappe.copy_doc(service_record)

                        # Update the linked_service field to the Grey Area doc
                        new_service_doc.linked_doctype = "Grey Area" 
                        new_service_doc.linked_service = grey_area_doc.name

                        # Insert the copied service document
                        new_service_doc.insert(ignore_permissions=True, ignore_mandatory=True)

                # Archive the lead after updating the linked services
                lead_doc.custom_archive = 1
                lead_doc.custom_grey_area = grey_area_doc.name
                lead_doc.save(ignore_permissions=True)
            else:
                throw(_(f"{lead_name}: Pipeline status must be 'Win' or 'Lost Fit'"))

        return {"message": "Leads moved to Grey Area and services updated successfully."}

    except Exception as e:
        frappe.throw(str(e))
    

def archive_leads():
    leads = frappe.db.get_all(
        "Lead",
        filters={
            "custom_pipeline_status": "Lost Not Fit",
            "custom_archive": 0
        },
        fields=["name"]
    )
    if leads:
        move_to_grey_area = frappe.db.get_single_value('Global Settings', 'move_to_grey_area')
        if getdate() >= add_to_date(move_to_grey_area, days=1):
            for lead in leads:
                doc = frappe.get_doc("Lead", lead.name)
                doc.db_set("custom_archive", 1, update_modified=False)
