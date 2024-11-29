import frappe
from frappe.model.document import Document
from kreston.methods.lead import services
from kreston.kreston.doctype.pmo_assignment_details.pmo_assignment_details import create_pmo_assignment


class PMOClient(Document):
    pass


def move_from_lead_to_pmo_client(doc, method=None):
    try:
        services_link = []
        old_doc = doc.get_doc_before_save()

        # Check if the custom_pipeline_status field is updated
        status_updated = old_doc and old_doc.custom_pipeline_status != doc.custom_pipeline_status

        if status_updated and doc.custom_pipeline_status == "Win":
            # Create a new PMO Client document
            pmo_client_doc = frappe.new_doc("PMO Client")

            # Fetch field metadata for Lead and PMO Client
            lead_fields = {field.fieldname for field in frappe.get_meta("Lead").fields}
            pmo_client_fields = {field.fieldname for field in frappe.get_meta("PMO Client").fields}

            # Copy matching fields from Lead to PMO Client
            for fieldname in lead_fields.intersection(pmo_client_fields):
                pmo_client_doc.set(fieldname, doc.get(fieldname))

            # Link the Lead to the PMO Client
            pmo_client_doc.lead = doc.name

            # Insert the new PMO Client document
            pmo_client_doc.insert(ignore_permissions=True, ignore_mandatory=True)

            # Loop through the services and dynamically copy fields
            for service in services:
                # Fetch service records where linked_service matches the Lead's name
                service_docs = frappe.get_all(
                    service,
                    filters={"linked_service": doc.name},
                    fields=["name"]
                )

                # Fetch metadata for the service doctype and the target PMO Service Budget doctype
                service_fields = {field.fieldname for field in frappe.get_meta(service).fields}
                pmo_service_fields = {field.fieldname for field in frappe.get_meta("PMO Service Budget").fields}

                for service_doc in service_docs:
                    # Fetch the service record
                    service_record = frappe.get_doc(service, service_doc["name"])

                    # Create a new document instance for PMO Service Budget
                    new_service_doc = frappe.new_doc("PMO Service Budget")

                    # Copy matching fields dynamically
                    for fieldname in service_fields.intersection(pmo_service_fields):
                        new_service_doc.set(fieldname, service_record.get(fieldname))

                    # Set additional fields for the new service document
                    new_service_doc.update({
                        "linked_doctype": "PMO Client",
                        "linked_service": pmo_client_doc.name,
                        "service_type": service,
                    })

                    # Insert the new service document
                    new_service_doc.insert(ignore_permissions=True, ignore_mandatory=True)
                    new_service_doc.reload()

                    # Create a PMO assignment for the new service document
                    create_pmo_assignment(new_service_doc)

                    # Append to services_link
                    services_link.append({
                        "service_type": service,
                        "service_budget": new_service_doc.name
                    })

            # Update and save the PMO Client with services_link
            pmo_client_doc.set("services_link", services_link)
            pmo_client_doc.save(ignore_permissions=True)

            frappe.msgprint(f"Lead {doc.name} successfully moved to PMO Client.")
            return {"message": "Lead moved to PMO Client and services updated successfully."}

    except Exception as e:
        frappe.throw(f"Error during lead-to-PMO Client conversion: {str(e)}")
