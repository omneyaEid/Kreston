# Copyright (c) 2024, omneyaeid827@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PMOAssignmentDetails(Document):
	pass


def calc_total_hours(doc):
	"""Calculate total hours based on the audit_budget_table."""
	total_hours = sum([float(task.hour_no or 0) for task in doc.audit_budget_table])
	return total_hours

def populate_budget_fields(doc):
	"""Populate and return a dictionary of employees assigned to each portfolio level."""
	# Initialize the final result dictionary
	level_to_employee = {}

	# Store the employee for the last available level
	previous_employee = None

	# Iterate through the budget table, processing the levels
	for entry in doc.audit_budget_table:
		level = int(entry.get("portfolio_level"))
		employee = entry.get("employee")

		# If the employee field is empty, use the previous available employee
		if employee:
			previous_employee = employee
		elif not employee and previous_employee:
			employee = previous_employee

		# Store the employee value for the current level
		level_to_employee[level] = employee

	# Fill missing levels by carrying over from the previous level
	# Loop through all levels from 1 to 5
	for level in range(1, 6):
		if level not in level_to_employee:
			level_to_employee[level] = previous_employee

	# Create the desired output format {"p1": employee, "p2": employee, ...}
	employee_by_level = {f"p{level}": employee for level, employee in level_to_employee.items()}

	return employee_by_level

def create_pmo_assignment(doc):
	"""Create a PMO Assignment Details document based on the current PMO Service Budget."""
	# Create a new assignment document
	assignment = frappe.new_doc("PMO Assignment Details")
	
	# Set values for the assignment document
	assignment.client = doc.linked_service
	assignment.service_type = doc.service_type
	assignment.total_budget_hour = calc_total_hours(doc)
	assignment.variances_by_number = calc_total_hours(doc)
	
	# Get the employee assignments for each level
	employee_by_level = populate_budget_fields(doc)
	
	# Assign employees to p1, p2, p3, p4, p5 from the populated dictionary
	assignment.p1 = employee_by_level.get("p1")
	assignment.p2 = employee_by_level.get("p2")
	assignment.p3 = employee_by_level.get("p3")
	assignment.p4 = employee_by_level.get("p4")
	assignment.p5 = employee_by_level.get("p5")
	
	# Insert the assignment document into the database
	assignment.insert(ignore_permissions=True, ignore_mandatory=True)
