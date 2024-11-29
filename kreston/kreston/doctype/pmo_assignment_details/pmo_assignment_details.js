// Copyright (c) 2024, omneyaeid827@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("PMO Assignment Details", {
    refresh(frm) {
        if (!frm.is_new()) {
            let service_type = frm.doc.service_type;

            if (service_type) {
                // Remove the word "service" (case-insensitive) from service_type
                let sanitized_service_type = service_type.replace(/service/gi, "").trim();

                // Add a filter to the field where job_status is linked
                frm.set_query("job_status", function () {
                    return {
                        filters: {
                            service_type: ["like", `%${sanitized_service_type}%`]
                        }
                    };
                });
            }
        }
    },
});
