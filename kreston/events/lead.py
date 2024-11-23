import frappe
from frappe.utils import getdate
from frappe.client import get_count

def after_insert(doc,method=None):
    doc.custom_opening_date = getdate()


def on_update(doc, method=None):
    # Get the document state before the current save
    old_doc = doc.get_doc_before_save()
    
    # Check if the custom_pipeline_status has been updated
    status_updated = old_doc and old_doc.custom_pipeline_status != doc.custom_pipeline_status
    
    # Check if this is a new document
    new_status = old_doc is None
    
    # If the status has changed or this is a new document and the new status is "Win"
    if (status_updated or new_status) and doc.custom_pipeline_status == "Win":
        if doc.custom_pipeline_status == "Win":
            # Set the custom_client_number
            doc.custom_client_number = 400 + get_last_sequance()
        else:
            doc.custom_client_number = ""
    
    if status_updated and doc.custom_pipeline_status in ["Lost Fit", "Lost Not Fit"]:
        doc.custom_last_status = old_doc.custom_pipeline_status


def validate(doc, method=None):
    service_mapping = {
        "custom_audit": "Audit Service",
        "custom_audit_sp": "Audit SP Service",
        "custom_z_cases": "Z Cases Service",
        "custom_zdp_sp": "ZDP SP Service",
        "custom_vat": "VAT Service",
        "custom_vat_cases": "VAT Cases Service",
        "custom_aup": "AUP Service",
        "custom_lc": "LC Service",
        "custom_zakat": "Zakat Service",
        "custom_tax": "Tax Service",
        "custom_som": "SOM Service",
        "custom_vdp_sp": "VDP SP Service",
    }

    missing_services = []

    for custom_field, service_type in service_mapping.items():
        # Check if the custom field on the doc is set to 1 (True)
        if getattr(doc, custom_field, 0) == 1:
            # Fetch the service linked to this document (doc.name) from the corresponding service Doctype
            linked_services = frappe.get_all(
                service_type,  # Dynamically refer to the Doctype from the mapping
                filters={"linked_service": doc.name},
                fields=["name"]
            )

            # If no linked service is found, add to missing_services list
            if not linked_services:
                missing_services.append(service_type)

    if not doc.is_new():
        doc_before_save = frappe.get_doc(doc.doctype, doc.name, for_update=True)

        # If there are any missing services, throw a validation error listing all
        if doc_before_save.custom_pipeline_status == "Proposal" and(
            doc_before_save.custom_pipeline_status != doc.custom_pipeline_status
        ):
            if missing_services:
                missing_list = ",".join(missing_services)
                frappe.throw(f"The following required services are missing for {doc.name}:\n{missing_list}")


def get_last_sequance():
    # Count the number of Leads with custom_pipeline_status set to "Win"
    return get_count(doctype="Lead", filters={"custom_pipeline_status": "Win"}, cache=True)
