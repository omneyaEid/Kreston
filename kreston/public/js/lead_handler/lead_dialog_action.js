// Copyright (c) 2024, omneyaeid827@gmail.com and contributors
// For license information, please see license.txt

// Function to toggle related amount fields when a check field is checked
function toggle_related_field(dialog, check_fieldname, related_fieldname) {
    const is_checked = dialog.get_value(check_fieldname);
    dialog.set_df_property(related_fieldname, 'hidden', !is_checked);
}

// Function to update total_fee based on hour_no and hour_fee
function update_total_fee(dialog, employee_change) {
    let budget_table = dialog.get_value("audit_budget_table");

    if (Array.isArray(budget_table)) {
        budget_table.forEach((row, index) => {
            if (employee_change) {
                // Fetch the employee data (position and hour_fee) from the Employee doctype
                frappe.db.get_value("Employee", row.employee, ["designation", "custom_hour_fee"], (result) => {
                    if (result) {
                        // Set position and hour_fee from the fetched employee data
                        budget_table[index].position = result.designation || ''; // Set the designation/position
                        if (budget_table[index].hour_fee != result.custom_hour_fee) {
                            budget_table[index].hour_fee = parseFloat(result.custom_hour_fee) || 0; // Set the hour fee
                            const hours = parseFloat(budget_table[index].hour_no) || 0;
                            const fee_per_hour = parseFloat(budget_table[index].hour_fee) || 0;
                            budget_table[index].total_fee = hours * fee_per_hour; // Calculate total fee
                        }
                        dialog.set_value("audit_budget_table", budget_table);
                        const budget_table_grid = dialog.fields_dict.audit_budget_table.grid; // Get the grid object
                        budget_table_grid.refresh();
                    }
                });

            } else {
                const hours = parseFloat(row.hour_no) || 0;
                const fee_per_hour = parseFloat(row.hour_fee) || 0;
                row.total_fee = hours * fee_per_hour; // Calculate total fee
                const budget_table_grid = dialog.fields_dict.audit_budget_table.grid; // Get the grid object
                budget_table_grid.refresh();
            }
        });

        // Update the total_audit_budget and total_audit_expenses after updating fees
        calculate_total_audit_budget(dialog);
        calculate_total_audit_expenses(dialog);
    }

}

// Function to calculate the total audit budget
function calculate_total_audit_budget(dialog) {
    const budget_table = dialog.get_value("audit_budget_table");
    let total_audit_budget = 0;

    if (Array.isArray(budget_table)) {
        total_audit_budget = budget_table.reduce((total, row) => {
            return total + (parseFloat(row.total_fee) || 0);
        }, 0);
    }

    dialog.set_value("total_audit_budget", total_audit_budget);
}

// Function to calculate total audit expenses
function calculate_total_audit_expenses(dialog) {
    const per_diem = parseFloat(dialog.get_value("audit_per_diem_amount")) || 0;
    const car_amount = parseFloat(dialog.get_value("audit_car_amount")) || 0;
    const ticket_amount = parseFloat(dialog.get_value("audit_ticket_amount")) || 0;
    const other_amount = parseFloat(dialog.get_value("audit_other_amount")) || 0;

    const total_expenses = per_diem + car_amount + ticket_amount + other_amount;
    dialog.set_value("total_audit_expenses", total_expenses);
}
