frappe.ui.form.on("Lead", {
    refresh: function (frm) {
        // Any setup actions for the Lead doctype
    }
});

frappe.ui.form.on("Audit Budget Table", {
    hour_no: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        let hour_no = parseFloat(row.hour_no) || 0;
        let hour_fee = parseFloat(row.hour_fee) || 0;

        // Assuming total_fee should be hour_no * hour_fee
        let total_fee = hour_no * hour_fee;
        
        // Set the calculated total_fee
        frappe.model.set_value(cdt, cdn, "total_fee", total_fee);
    },
    hour_fee: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        let hour_no = parseFloat(row.hour_no) || 0;
        let hour_fee = parseFloat(row.hour_fee) || 0;

        // Assuming total_fee should be hour_no * hour_fee
        let total_fee = hour_no * hour_fee;
        
        // Set the calculated total_fee
        frappe.model.set_value(cdt, cdn, "total_fee", total_fee);
    }
});
