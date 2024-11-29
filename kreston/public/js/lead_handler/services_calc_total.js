function calculate_row_total(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	let hour_no = parseFloat(row.hour_no) || 0;
	let hour_fee = parseFloat(row.hour_fee) || 0;

	// Calculate total fee for the row
	let total_fee = hour_no * hour_fee;

	// Set the calculated total_fee for the row
	frappe.model.set_value(cdt, cdn, "total_fee", total_fee);
}

function calculate_total_audit_budget(frm) {
	let total_audit_budget = 0;

	// Check if audit_budget_table is defined and is an array
	if (frm.doc.audit_budget_table && Array.isArray(frm.doc.audit_budget_table)) {
		frm.doc.audit_budget_table.forEach(row => {
			total_audit_budget += parseFloat(row.total_fee) || 0;
		});
	}

	// Set the total_audit_budget value in the parent form
	frm.set_value("total_audit_budget", total_audit_budget);

	// Refresh the field to ensure the UI updates
	frm.refresh_field("total_audit_budget");
}

function calculate_total_audit_expenses(frm) {
	// Parse all amounts to ensure they are numbers (or default to 0 if undefined or NaN)
	let audit_per_diem_amount = parseFloat(frm.doc.audit_per_diem_amount) || 0;
	let audit_car_amount = parseFloat(frm.doc.audit_car_amount) || 0;
	let audit_ticket_amount = parseFloat(frm.doc.audit_ticket_amount) || 0;
	let audit_other_amount = parseFloat(frm.doc.audit_other_amount) || 0;

	// Calculate the total audit expenses
	let total_audit_expenses = audit_per_diem_amount + audit_car_amount + audit_ticket_amount + audit_other_amount;

	// Set the total_audit_expenses value in the form
	frm.set_value("total_audit_expenses", total_audit_expenses);

	// Refresh the field to ensure the UI updates
	frm.refresh_field("total_audit_expenses");
}



function calculate_total_hours_and_risk_level(frm) {
	let total_hours = 0;

	// Check if the audit_budget_table exists and has data
	if (frm.doc.audit_budget_table && frm.doc.audit_budget_table.length > 0) {
		frm.doc.audit_budget_table.forEach(row => {
			// Ensure hour_no is a valid number
			let hours = parseInt(row.hour_no, 10);
			if (!isNaN(hours)) {
				total_hours += hours;
			}
		});
	}

	// Set the total hours value in the form
	frm.set_value('total_hours', total_hours);

	// Calculate risk management level based on total_hour_no
	let risk_level = 'Low'; // Default value

	if (total_hours > 120) {
		risk_level = 'High';
	} else if (total_hours >= 81) {
		risk_level = 'Modorate';
	}

	// Set the risk_management_level field in the form
	frm.set_value('risk_management_level', risk_level);
}