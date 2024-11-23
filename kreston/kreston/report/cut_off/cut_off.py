# Copyright (c) 2024, omneyaeid827@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import datetime
from frappe.utils import flt


pipeline_status = [
	'Prospect',
	'Proposal',
	'Engagement Letter',
	'Win Completed',
	'Win In-Complete',
	'Lost Fit',
	'Lost Not Fit'
]


def execute(filters=None):
    from_year = int(filters.get("from_year"))
    to_year = int(filters.get("to_year"))

    validate_years(from_year, to_year)

    columns = get_columns(from_year, to_year)
    data = []

    # Initialize data with statuses
    for status in pipeline_status:
        row = {'status': status}
        # Add year columns initialized to 0
        for year in range(from_year, to_year + 1):
            year_label = f"{year}-{year + 1}"
            row[year_label] = 0
        data.append(row)

    # Populate data with total amounts per year
    for row in data:
        status = row['status']
        for year in range(from_year, to_year):
            year_label = f"{year}-{year + 1}"
            total = get_grey_area_total_amount(year, year + 1, status)
            row[year_label] = total

    # Add a total row (excluding "Lost Not Fit")
    net_row = {'status': '<strong>Net</strong>'}
    net_row_without_lost = {'status': '<strong>Net (Without Lost Not Fit)</strong>'}
    
    for year in range(from_year, to_year):
        year_label = f"{year}-{year + 1}"
        net_row[year_label] = sum(flt(row[year_label]) for row in data)
        net_row_without_lost[year_label] = sum(
            flt(row[year_label]) for row in data if row['status'] != 'Lost Not Fit'
        )

    # Append both net rows and a separator
    data.extend([net_row, net_row_without_lost, {}])

    # Process the second set of data (data2)
    data2 = []
    
    # Initialize data2 with statuses
    for status in pipeline_status:
        row = {'status': status}
        # Add year columns initialized to 0
        for year in range(from_year, to_year + 1):
            year_label = f"{year}-{year + 1}"
            row[year_label] = 0
        data2.append(row)

    # Populate data2 with lead total amounts per year
    for row in data2:
        status = row['status']
        for year in range(from_year, to_year):
            year_label = f"{year}-{year + 1}"
            total = get_lead_total_amount(year, year + 1, status)
            row[year_label] = total

    # Add net row to data2
    net_row_data2 = {'status': '<strong>Net</strong>'}
    net_row2_without_lost = {'status': '<strong>Opening Pipeline</strong>'}

    for year in range(from_year, to_year):
        year_label = f"{year}-{year + 1}"
        net_row_data2[year_label] = sum(flt(row[year_label]) for row in data2)

        # Avoid calculating for years before from_year
        if year > from_year:
            pre_year_label = f"{year - 1}-{year}"
            net_row2_without_lost[year_label] = sum(
                flt(row[pre_year_label]) for row in data2 if row['status'] != 'Lost Not Fit'
            )
        else:
            net_row2_without_lost[year_label] = 0  # No prior year available for the first year

    data2.append(net_row_data2)

    # Finally, extend data with data2
    data.extend(data2)
    data.insert(0, net_row2_without_lost)

    return columns, data

	
def validate_years(from_year, to_year):
	if not from_year or not to_year:
		frappe.throw(_("Please select years."))
	if int(from_year) > int(to_year):
		frappe.throw(_("From Year cannot be after To Year."))


def get_grey_area_total_amount(from_year, to_year, status):
	from_date = datetime.date(from_year, 7, 1)
	to_date = datetime.date(to_year, 6, 27)

	query = """
		SELECT SUM(custom_net_total_budget)
		FROM `tabGrey Area`
		WHERE custom_archive = 1 AND custom_opening_date BETWEEN %(from_date)s AND %(to_date)s
	"""
	# Add status conditions
	if status == 'Win Completed':
		query += "AND custom_pipeline_status = 'Win' AND custom_win_status = 'Complete'"
	elif status == 'Win In-Complete':
		query += "AND custom_pipeline_status = 'Win' AND custom_win_status = 'In-Complete'"
	else:
		query += f"AND custom_pipeline_status = '{status}'"

	net_total_lead = frappe.db.sql(query, {'from_date': from_date, 'to_date': to_date})
	net_total = net_total_lead[0][0] if net_total_lead else 0

	return flt(net_total)


def get_lead_total_amount(from_year, to_year, status):
	from_date = datetime.date(from_year, 7, 1)
	to_date = datetime.date(to_year, 6, 27)

	query = """
		SELECT SUM(custom_net_total_budget)
		FROM `tabLead` ld
		WHERE custom_archive = 0 AND custom_opening_date BETWEEN %(from_date)s AND %(to_date)s
	"""
      
	# Add status conditions
	if status == 'Win Completed':
		query += """AND custom_pipeline_status = 'Win' AND custom_win_status = 'Complete'"""
	elif status == 'Win In-Complete':
		query += """AND custom_pipeline_status = 'Win' AND custom_win_status = 'In-Complete'"""
	else:
		query += f"AND custom_pipeline_status = '{status}'"

	net_total_lead = frappe.db.sql(query, {'from_date': from_date, 'to_date': to_date})
	net_total = net_total_lead[0][0] if net_total_lead else 0

	return flt(net_total)


def get_columns(from_year, to_year):
	columns = [
		{
			"label": "",
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 180,
		}
	]

	for i in range(int(to_year)- int(from_year)):
		name = ("{0}-{1}").format(int(from_year)+i, int(from_year)+i+1)
		columns.append({
			"label": name,
			"fieldname": name,
			"fieldtype": "Currency",
			"width": 180,
		})
	
	return columns