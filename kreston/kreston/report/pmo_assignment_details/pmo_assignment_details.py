# Copyright (c) 2024, omneyaeid827@gmail.com and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    for row in data:
        row["button"] = (
            f'<a href="/app/pmo-assignment-details/{row.name}" '
            f'data-doctype="PMO Assignment Details" data-name="{row.name}" data-value="{row.name}" '
            f'style="color: white; background-color: black; text-decoration: none; font-weight: bold; '
            f'padding: 0px 35px; border-radius: 5px; display: inline-block; border: none; cursor: pointer;">'
            f'Action</a>'
        )
    return columns, data

def get_data(filters=None):
    return frappe.db.get_list(
        "PMO Assignment Details",
        fields=[
            "name",
            "client",
            "client_name",
            "p1",
            "p2",
            "p3",
            "p4",
            "p5",
            "service_type",
            "total_actual_hour",
            "total_budget_hour",
            "variances_by_number",
            "variances_percentage",
        ],
    )

def get_columns():
    return [
        {
            "label": "ID",
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "PMO Assignment Details",
            "width": 150,
        },
        {
            "label": "Client",
            "fieldname": "client",
            "fieldtype": "Link",
            "options": "PMO Client",
            "width": 150,
        },
        {
            "label": "Client Name",
            "fieldname": "client_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "P1",
            "fieldname": "p1",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": "P2",
            "fieldname": "p2",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": "P3",
            "fieldname": "p3",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": "P4",
            "fieldname": "p4",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": "P5",
            "fieldname": "p5",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": "Service Type",
            "fieldname": "service_type",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Total Budget Hours",
            "fieldname": "total_budget_hour",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": "Total Actual Hours",
            "fieldname": "total_actual_hour",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": "Variance (Number)",
            "fieldname": "variances_by_number",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": "Variance (%)",
            "fieldname": "variances_percentage",
            "fieldtype": "Percent",
            "width": 150,
        },
        {
            "label": "Action",
            "fieldname": "button",
            "fieldtype": "HTML",
            "width": 180,
        },
    ]
