// Copyright (c) 2024, omneyaeid827@gmail.com and contributors
// For license information, please see license.txt

function fetchAndSetLeadTotals(frm) {
    // Call the server-side method to get the totals
    if (!frm.is_new()) { // Ensure the form is not new
        frappe.call({
            method: "kreston.methods.lead.calc_lead_totals",
            args: {
                doctype: frm.doc.doctype,
                name: frm.doc.name
            },
            callback: function (response) {
                if (response.message) {
                    // Assuming response.message is an object with the totals
                    const totals = response.message;

                    // Calculate the net total budget
                    const net_total_budget = (totals.total_audit_budget || 0) +
                        (totals.total_audit_expenses || 0) +
                        (totals.audit_write_up_down || 0);

                    // Store previous values to check for changes
                    const previous_total_budget = frm.doc.custom_total_services_budget;
                    const previous_total_expenses = frm.doc.custom_total_services_expenses;
                    const previous_write_updown = frm.doc.custom_total_write_updown;

                    // Set values in the form
                    frm.set_value("custom_total_services_budget", totals.total_audit_budget || 0);
                    frm.set_value("custom_total_services_expenses", totals.total_audit_expenses || 0);
                    frm.set_value("custom_total_write_updown", totals.audit_write_up_down || 0);
                    frm.set_value("custom_net_total_budget", net_total_budget);

                    // Optionally, refresh the field display if needed
                    frm.refresh_field("custom_total_services_budget");
                    frm.refresh_field("custom_total_services_expenses");
                    frm.refresh_field("custom_total_write_updown");
                    frm.refresh_field("custom_net_total_budget");

                    // Check for changes and save if there are changes
                    if (frm.doc.custom_total_services_budget !== previous_total_budget ||
                        frm.doc.custom_total_services_expenses !== previous_total_expenses ||
                        frm.doc.custom_total_write_updown !== previous_write_updown) {
                        frm.save(null, function () {
                            // Success callback
                            frappe.show_alert({ message: "Changes saved successfully!", indicator: 'green' });
                        }, function () {
                        });
                    }
                }
            }
        });
    }
}