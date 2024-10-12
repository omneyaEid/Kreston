// Copyright (c) 2024, omneyaeid827@gmail.com and contributors
// For license information, please see license.txt

function updateStatusHandler(frm) {
    if (frm.doc.custom_pipeline_status === "Win") {
        frm.set_value("custom_legal_company_name", frm.doc.custom_company_name_card || "");
        frm.refresh_field("custom_legal_company_name");
    }
    if (["Win","Lost Not Fit"].includes(frm.doc.custom_pipeline_status)) {
        frm.set_df_property("custom_followup_date", "hidden", 1);
    }
}

function saveStatusHandler(frm){
    if (["Win", "Lost Fit", "Lost Not Fit"].includes(frm.doc.custom_pipeline_status)) {
        const current_date = frappe.datetime.now_date(); // Get the current date
        frm.set_value("custom_closing_date", current_date); // Set the current date directly
        frm.refresh_field("custom_closing_date");
        frm.set_df_property("custom_closing_date", "read_only", 1);
    }
}

function decisionHandler(frm) {
    if (frm.doc.custom_decision === "Reject") {
        const current_date = frappe.datetime.now_date(); // Get the current date

        frm.set_value("custom_pipeline_status", "Lost Not Fit");
        frm.set_value("custom_closing_date", current_date); // Set the current date directly

        // Refresh the fields
        frm.refresh_field("custom_pipeline_status");
        frm.refresh_field("custom_closing_date");

        // Set the custom_closing_date field to read-only
        frm.set_df_property("custom_closing_date", "read_only", 1);
    }
}
