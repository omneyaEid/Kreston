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
                if grey_area_doc.custom_pipeline_status == "Win" and grey_area_doc.custom_win_status == "In-Complete":
                    if fieldname in lead_fields:
                        new_lead_doc.set(fieldname, grey_area_doc.get(fieldname))
                else:
                    if fieldname in lead_fields and (fieldname not in ignored_fields):
                        new_lead_doc.set(fieldname, grey_area_doc.get(fieldname))
            
            new_lead_doc.custom_pipeline_status = grey_area_doc.new_pipeline_status if grey_area_doc.new_pipeline_status else grey_area_doc.custom_pipeline_status
            new_lead_doc.custom_last_status = grey_area_doc.custom_last_status

            # Insert the new Lead document
            new_lead_doc.custom_archive = 0
            new_lead_doc.custom_grey_area = None

            new_lead_doc.flags.ignore_validate = True
            new_lead_doc.insert(ignore_permissions=True, ignore_mandatory=True)
            

            # # Update linked services from Grey Area to new Lead
            # for service in services:
            #     # Fetch all service records linked to the grey_area_name
            #     service_docs = frappe.get_all(
            #         service,
            #         filters={"linked_service": grey_area_name},
            #         fields=["name", "linked_service"]
            #     )

            #     # Update each service to link to the new Lead
            #     for service_doc in service_docs:
            #         service_record = frappe.get_doc(service, service_doc["name"])
            #         service_record.linked_service = new_lead_doc.name
            #         service_record.linked_doctype = "Lead"
            #         service_record.save(ignore_permissions=True)

            # Optionally delete the Grey Area document after moving the services
            grey_area_doc.custom_archive = 1
            grey_area_doc.save(ignore_permissions=True)

        return {"message": "Grey Area documents moved to Lead and services updated successfully."}

    except Exception as e:
        frappe.throw(str(e))



ignored_fields = [
  "custom_opkokfgfdgproposal",
  "custom_f_s_l",
  "custom_ifrs",
  "custom_column_break_s0pgt",
  "custom_company_type",
  "custom_institution_nationality",
  "custom_specify_nationality",
  "custom_acceptance_decision",
  "custom_acceptance",
  "custom_column_break_wffmq",
  "custom_acceptance_letter",
  "custom_column_break_wppxc",
  "custom_comments",
  "custom_column_break_1tzzm",
  "custom_decision",
  "custom_services_budget",
  "custom_audit",
  "custom_add1",
  "custom_to_be_consider_in_quaem",
  "custom_audit_sp",
  "custom_audit_sp_type",
  "custom_add2",
  "custom_z_cases",
  "custom_add3",
  "custom_zdp_sp",
  "custom_add4",
  "custom_column_break_bo41i",
  "custom_vat",
  "custom_add5",
  "custom_vat_cases",
  "custom_add6",
  "custom_aup",
  "custom_add7",
  "custom_lc",
  "custom_add8",
  "custom_column_break_ygnvq",
  "custom_zakat",
  "custom_add9",
  "custom_tax",
  "custom_add10",
  "custom_som",
  "custom_add11",
  "custom_vdp_sp",
  "custom_add12",
  "custom_engagement_letter",
  "custom_note",
  "custom_section_break_dhgiu",
  "custom_physical_year2",
  "custom_column_break_mdxra",
  "custom_f_s_types",
  "custom_win",
  "custom_win_status",
  "section_break_cibw",
  "custom_legal_company_name",
  "custom_english_company_name",
  "custom_column_break_foqr0",
  "custom_commercial_registry_number",
  "custom_client_number",
  "custom_column_break_cs2jn",
  "custom_commercial_registry",
  "custom_other_attachments",
  "custom_section_break_g8aoi",
  "custom_customer_activities",
  "custom_lost_fit",
  "custom_reason",
  "custom_column_break_u5oxx",
  "custom_next_season_followup_date",
  "custom_column_break_s9ftq",
  "custom_last_status_before_closing",
  "custom_section_break_bobdx",
  "custom_lostfit_comments",
  "custom_lost_not_fit",
  "custom_lost_not_fit_reason",
  "custom_column_break_3zqhe",
  "custom_lost_not_fit__last_status_before_closing",
  "custom_section_break_nu3hw",
  "custom_lostnotfit_comments",
  "custom_general",
  "custom_pipeline_status",
  "custom_last_status",
  "column_break_hjza",
  "new_pipeline_status",
  "custom_section_break_gv0qd",
  "custom_opening_date",
  "custom_column_break_lninh",
  "custom_followup_date",
  "custom_column_break_p0bfc",
  "custom_closing_date",
  "custom_totals",
  "custom_column_break_13wb1",
  "custom_total_services_budget",
  "custom_total_services_expenses",
  "custom_total_write_updown",
  "custom_net_total_budget"
 ]