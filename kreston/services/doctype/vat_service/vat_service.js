// Copyright (c) 2024, omneyaeid827@gmail.com and contributors
// For license information, please see license.txt

{% include 'kreston/public/js/lead_handler/services_calc_total.js' %}

frappe.ui.form.on("VAT Service", {
	refresh: function (frm) {
		calculate_total_audit_budget(frm);
	},
	audit_per_diem_amount: function (frm) {
		calculate_total_audit_expenses(frm);
	},
	audit_car_amount: function (frm) {
		calculate_total_audit_expenses(frm);
	},
	audit_ticket_amount: function (frm) {
		calculate_total_audit_expenses(frm);
	},
	audit_other_amount: function (frm) {
		calculate_total_audit_expenses(frm);
	},
	before_save: function(frm) {
        calculate_total_hours_and_risk_level(frm);
    }
});

frappe.ui.form.on("Service Budget", {
	hour_no: function (frm, cdt, cdn) {
		calculate_row_total(frm, cdt, cdn);
		calculate_total_audit_budget(frm);
	},
	hour_fee: function (frm, cdt, cdn) {
		calculate_row_total(frm, cdt, cdn);
		calculate_total_audit_budget(frm);
	},
	total_fee: function (frm, cdt, cdn) {
		calculate_total_audit_budget(frm);
	}
});
