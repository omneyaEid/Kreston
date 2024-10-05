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


def get_last_sequance():
    # Count the number of Leads with custom_pipeline_status set to "Win"
    return get_count(doctype="Lead", filters={"custom_pipeline_status": "Win"}, cache=True)
