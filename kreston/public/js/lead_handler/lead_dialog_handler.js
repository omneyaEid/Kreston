// Copyright (c) 2024, omneyaeid827@gmail.com and contributors
// For license information, please see license.txt

{% include 'kreston/public/js/lead_handler/lead_dialog_action.js' %}

// Define a function to create the dialog
function createAuditDialog(frm, title, doctype) {
    // Create the dialog
    let dialog = new frappe.ui.Dialog({
        title: title,
        fields: [
            {
                fieldname: "audit_group_leader",
                fieldtype: "Link",
                label: "Audit Group Leader",
                options: "Employee",
                reqd: 1
            },
            {
                fieldtype: "Table",
                fieldname: "audit_budget_table",
                label: "Audit Budget",
                reqd: 1,
                fields: [
                    {
                        fieldname: "employee",
                        fieldtype: "Link",
                        in_list_view: 1,
                        label: "Employee",
                        options: "Employee",
                        reqd: 1,
                        onchange: function () {
                            update_total_fee(dialog, true); // Call the function to update total_fee
                        }
                    },
                    {
                        fieldname: "position",
                        fieldtype: "Data",
                        in_list_view: 1,
                        label: "Position"
                    },
                    {
                        fieldtype: "Float",
                        in_list_view: 1,
                        fieldname: "hour_no",
                        label: "Number of Hours",
                        default: 0,
                        onchange: function () {
                            update_total_fee(dialog, false); // Call the function to update total_fee
                        }
                    },
                    {
                        fieldtype: "Float",
                        in_list_view: 1,
                        fieldname: "hour_fee",
                        label: "Fee per Hour",
                        default: 0,
                        onchange: function () {
                            update_total_fee(dialog, false); // Call the function to update total_fee
                        }
                    },
                    {
                        fieldtype: "Float",
                        in_list_view: 1,
                        fieldname: "total_fee",
                        label: "Total Fee",
                        read_only: 1
                    }
                ]
            },
            {
                fieldtype: "Float",
                fieldname: "total_audit_budget",
                label: "Total Audit Budget",
                read_only: 1
            },
            {
                fieldtype: "Float",
                fieldname: "audit_write_up_down",
                label: "Audit Write Up/Down"
            },
            {
                fieldtype: "Check",
                fieldname: "audit_per_diem",
                label: "Audit Per Diem",
                default: 0,
                onchange: function () {
                    toggle_related_field(dialog, "audit_per_diem", "audit_per_diem_amount");
                }
            },
            {
                fieldtype: "Float",
                fieldname: "audit_per_diem_amount",
                label: "Audit Per Diem Amount",
                onchange: () => calculate_total_audit_expenses(dialog),
                hidden: 1
            },
            {
                fieldtype: "Check",
                fieldname: "audit_cat",
                label: "Audit Car",
                default: 0,
                onchange: function () {
                    toggle_related_field(dialog, "audit_cat", "audit_car_amount");
                }
            },
            {
                fieldtype: "Float",
                fieldname: "audit_car_amount",
                label: "Audit Car Amount",
                onchange: () => calculate_total_audit_expenses(dialog),
                hidden: 1
            },
            {
                fieldtype: "Check",
                fieldname: "audit_ticket",
                label: "Audit Ticket",
                default: 0,
                onchange: function () {
                    toggle_related_field(dialog, "audit_ticket", "audit_ticket_amount");
                }
            },
            {
                fieldtype: "Float",
                fieldname: "audit_ticket_amount",
                label: "Audit Ticket Amount",
                onchange: () => calculate_total_audit_expenses(dialog),
                hidden: 1
            },
            {
                fieldtype: "Check",
                fieldname: "audit_other",
                label: "Other Audit Expenses",
                default: 0,
                onchange: function () {
                    toggle_related_field(dialog, "audit_other", "audit_other_amount");
                }
            },
            {
                fieldtype: "Float",
                fieldname: "audit_other_amount",
                label: "Other Audit Amount",
                onchange: () => calculate_total_audit_expenses(dialog),
                hidden: 1
            },
            {
                fieldtype: "Float",
                fieldname: "total_audit_expenses",
                label: "Total Audit Expenses",
                read_only: 1
            }
        ],
        primary_action: function () {
            const values = dialog.get_values();
            if (values) {
                // Calculate the total_audit_budget from the selected items
                let total_audit_budget = values.audit_budget_table.reduce((total, row) => {
                    return total + (parseFloat(row.total_fee) || 0);
                }, 0);

                // Now proceed to create the new Audit Service document
                frappe.call({
                    method: "frappe.client.insert",
                    args: {
                        doc: {
                            doctype: doctype,  // Use the provided doctype
                            linked_doctype: "Lead",
                            linked_service: frm.doc.name,
                            audit_group_leader: values.audit_group_leader,
                            audit_budget_table: values.audit_budget_table, // Use only selected items
                            total_audit_budget: total_audit_budget, // Total calculated from selected items
                            audit_write_up_down: values.audit_write_up_down,
                            audit_per_diem: values.audit_per_diem,
                            audit_per_diem_amount: values.audit_per_diem_amount,
                            audit_cat: values.audit_cat,
                            audit_car_amount: values.audit_car_amount,
                            audit_ticket: values.audit_ticket,
                            audit_ticket_amount: values.audit_ticket_amount,
                            audit_other: values.audit_other,
                            audit_other_amount: values.audit_other_amount,
                            total_audit_expenses: values.total_audit_expenses
                        }
                    },
                    callback: function (response) {
                        if (response && response.message) {
                            frappe.show_alert({
                                message: __("Audit Service Added"),
                                indicator: "green"
                            });
                            dialog.hide(); // Close the dialog
                        }
                    }
                });
            }
        },
        primary_action_label: "Save",
        on_show: function () {
            const budget_table = this.fields_dict.audit_budget_table.grid;
            budget_table.on("change", () => {
                calculate_total_audit_budget(dialog);
            });
        }
    });

    // Show the dialog
    dialog.show();
}
