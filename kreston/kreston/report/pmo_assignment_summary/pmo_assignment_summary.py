# Copyright (c) 2024, omneyaeid827@gmail.com and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_data(filters=None):
    conditions = []

    if filters:
        if filters.get("client"):
            conditions.append(f"client = '{filters['client']}'")
        if filters.get("client_name"):
            conditions.append(f"client_name LIKE '%{filters['client_name']}%'")
        if filters.get("service_type"):
            conditions.append(f"service_type LIKE '%{filters['service_type']}%'")
        for p in ["p1", "p2", "p3", "p4", "p5"]:
            if filters.get(p):
                conditions.append(f"{p} = '{filters[p]}'")
        if filters.get("assignment_date_in"):
            conditions.append(f"assignment_date_in >= '{filters['assignment_date_in']}'")
        if filters.get("assignment_date_out"):
            conditions.append(f"assignment_date_out <= '{filters['assignment_date_out']}'")
        if filters.get("job_status"):
            conditions.append(f"job_status = '{filters['job_status']}'")

    condition_query = " AND ".join(conditions) if conditions else "1=1"

    data = frappe.db.sql(
        f"""
        SELECT 
            name, client, service_type, client_name, p1, p2, p3, p4, p5, 
            total_actual_hour, total_budget_hour, variances_by_number, variances_percentage, 
            assignment_date_in, job_status, 
            assignment_date_out, progress
        FROM `tabPMO Assignment Details`
        WHERE {condition_query}
        """,
        as_dict=True,
    )

    return data


def get_columns():
    return [
        {"label": "ID", "fieldname": "name", "fieldtype": "Link", "options": "PMO Assignment Details", "width": 150},
        {"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "PMO Client", "width": 150},
        {"label": "Client Name", "fieldname": "client_name", "fieldtype": "Data", "width": 150},
        {"label": "Service Type", "fieldname": "service_type", "fieldtype": "Data", "width": 150},
        {"label": "P1", "fieldname": "p1", "fieldtype": "Link", "options": "Employee", "width": 100},
        {"label": "P2", "fieldname": "p2", "fieldtype": "Link", "options": "Employee",  "width": 100},
        {"label": "P3", "fieldname": "p3", "fieldtype": "Link", "options": "Employee",  "width": 100},
        {"label": "P4", "fieldname": "p4", "fieldtype": "Link", "options": "Employee",  "width": 100},
        {"label": "P5", "fieldname": "p5", "fieldtype": "Link", "options": "Employee",  "width": 100},
        {"label": "Total Budget Hours", "fieldname": "total_budget_hour", "fieldtype": "Float", "width": 150},
        {"label": "Total Actual Hours", "fieldname": "total_actual_hour", "fieldtype": "Float", "width": 150},
        {"label": "Variance (Number)", "fieldname": "variances_by_number", "fieldtype": "Float", "width": 150},
        {"label": "Variance (%)", "fieldname": "variances_percentage", "fieldtype": "Percent", "width": 150},
        {"label": "Assignment Date In", "fieldname": "assignment_date_in", "fieldtype": "Date", "width": 150},
        {"label": "Assignment Date Out", "fieldname": "assignment_date_out", "fieldtype": "Date", "width": 150},
        {"label": "Job Status", "fieldname": "job_status", "fieldtype": "Link", "options": "Job Status ", "width": 150},
        {"label": "Progress", "fieldname": "progress", "fieldtype": "Percent", "width": 150},
    ]
