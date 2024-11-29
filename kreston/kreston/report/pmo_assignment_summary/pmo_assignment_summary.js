// Copyright (c) 2024, omneyaeid827@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["PMO Assignment Summary"] = {
    "filters": [
        { "fieldname": "client", "label": "Client", "fieldtype": "Link", "options": "PMO Client" },
        { "fieldname": "client_name", "label": "Client Name", "fieldtype": "Data" },
        { "fieldname": "service_type", "label": "Service Type", "fieldtype": "Data" },
        { "fieldname": "p1", "label": "P1", "fieldtype": "Link", "options": "Employee" },
        { "fieldname": "p2", "label": "P2", "fieldtype": "Link", "options": "Employee" },
        { "fieldname": "p3", "label": "P3", "fieldtype": "Link", "options": "Employee" },
        { "fieldname": "p4", "label": "P4", "fieldtype": "Link", "options": "Employee" },
        { "fieldname": "p5", "label": "P5", "fieldtype": "Link", "options": "Employee" },
        { "fieldname": "assignment_date_in", "label": "Assignment Date In", "fieldtype": "Date" },
        { "fieldname": "assignment_date_out", "label": "Assignment Date Out", "fieldtype": "Date" },
        { "fieldname": "job_status", "label": "Job Status", "fieldtype": "Link", "options": "Job Status" },
    ]
};
