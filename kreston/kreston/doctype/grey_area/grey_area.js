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
        createAuditDialog(frm, "Add Audit Service", "Audit Service");
    },
    custom_add2: function (frm) {
        createAuditDialog(frm, "Add Audit SP Service", "Audit SP Service");
    },
    custom_add3: function (frm) {
        createAuditDialog(frm, "Add Z Cases Service", "Z Cases Service");
    },
    custom_add4: function (frm) {
        createAuditDialog(frm, "Add ZDP SP Service", "ZDP SP Service");
    },
    custom_add5: function (frm) {
        createAuditDialog(frm, "Add VAT Service", "VAT Service");
    },
    custom_add6: function (frm) {
        createAuditDialog(frm, "Add VAT Cases Service", "VAT Cases Service");
    },
    custom_add7: function (frm) {
        createAuditDialog(frm, "Add AUP Service", "AUP Service");
    },
    custom_add8: function (frm) {
        createAuditDialog(frm, "Add LC Service", "LC Service");
    },
    custom_add9: function (frm) {
        createAuditDialog(frm, "Add Zakat Service", "Zakat Service");
    },
    custom_add10: function (frm) {
        createAuditDialog(frm, "Add Tax Service", "Tax Service");
    },
    custom_add11: function (frm) {
        createAuditDialog(frm, "Add SOM Service", "SOM Service");
    }, custom_add12: function (frm) {
        createAuditDialog(frm, "Add VDP SP Service", "VDP SP Service");
    }
});
