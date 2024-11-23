// Copyright (c) 2024, omneyaeid827@gmail.com and contributors
// For license information, please see license.txt

{% include 'kreston/public/js/lead_handler/lead_dialog_handler.js' %}
{% include 'kreston/public/js/lead_handler/ui_handler.js' %}
{% include 'kreston/public/js/lead_handler/calc_totals.js' %}
{% include 'kreston/public/js/lead_handler/status_handler.js' %}

frappe.ui.form.on('Grey Area', {
    refresh: function(frm) {
        fetchAndSetLeadTotals(frm);
        updateHeadingColor(frm);

        if (!frm.is_new() && !frm.doc.custom_archive){
            frm.add_custom_button(__("Move To Pipline Content"), function(){
                if (!frm.doc.new_pipeline_status && frm.doc.custom_win_status != "In-Complete"){
                    frappe.throw(__("New Pipeline Status is required."));
                }

                if (frm.is_dirty()){
                    frappe.throw(__("You have unsaved changes in this form. Please save before you continue."))
                }

                // Call the server-side method to move the leads
                frappe.call({
                    method: "kreston.methods.grey_area.move_from_grey_area",
                    args: {
                        grey_area_names: [frm.doc.name]
                    },
                    callback: function (response) {
                        if (response.message) {
                            frappe.msgprint(response.message);
                            frm.reload_doc();
                        }
                    }
                });
            });
        }

        if (frm.doc.custom_archive){
            frm.disable_form();
        }
    },

    custom_audit: function(frm){
        updateHeadingColor(frm);
    },
    custom_pipeline_status: function(frm){
        updateStatusHandler(frm);
    },
    after_save: function (frm) {
        decisionHandler(frm);
    },
    custom_add1: function (frm) {
        createAuditDialog(frm, "Add Audit Service", "Audit Service", "Audit");
    },
    custom_add2: function (frm) {
        createAuditDialog(frm, "Add Audit SP Service", "Audit SP Service", "Audit SP");
    },
    custom_add3: function (frm) {
        createAuditDialog(frm, "Add Z Cases Service", "Z Cases Service", "Z Cases");
    },
    custom_add4: function (frm) {
        createAuditDialog(frm, "Add ZDP SP Service", "ZDP SP Service", "ZDP SP");
    },
    custom_add5: function (frm) {
        createAuditDialog(frm, "Add VAT Service", "VAT Service", "VAT");
    },
    custom_add6: function (frm) {
        createAuditDialog(frm, "Add VAT Cases Service", "VAT Cases Service", "VAT Cases");
    },
    custom_add7: function (frm) {
        createAuditDialog(frm, "Add AUP Service", "AUP Service", "AUP");
    },
    custom_add8: function (frm) {
        createAuditDialog(frm, "Add LC Service", "LC Service", "LC");
    },
    custom_add9: function (frm) {
        createAuditDialog(frm, "Add Zakat Service", "Zakat Service", "Zakat");
    },
    custom_add10: function (frm) {
        createAuditDialog(frm, "Add Tax Service", "Tax Service", "Tax");
    },
    custom_add11: function (frm) {
        createAuditDialog(frm, "Add SOM Service", "SOM Service", "SOM");
    }, custom_add12: function (frm) {
        createAuditDialog(frm, "Add VDP SP Service", "VDP SP Service", "VDP SP");
    }
});
