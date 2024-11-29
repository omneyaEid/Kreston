# Copyright (c) 2024, omneyaeid827@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class DailyTimeSheet(Document):
	def on_submit(self):
		"""Called when the timesheet is submitted. It triggers validation and updates PMO assignments."""
		self.validate_total_work()
		self.update_pmo_assignment()


	def validate_total_work(self):
		"""Validate that the total actual hours worked are at least 9 hours."""
		# Calculate the total actual hours worked
		total_actual_hours = sum([float(task.actual_hours or 0) for task in self.tasks])

		# Check if the total actual hours are less than 9
		if total_actual_hours < 9:
			# Raise an error if the total actual hours are less than 9
			frappe.throw(
				_("Total actual hours ({0}) are less than the required minimum of 9 hours.").format(
					total_actual_hours)
			)

	def update_pmo_assignment(self):
		"""Update the PMO Assignment with the total actual hours worked from the timesheet."""
		for task in self.tasks:
			# Get the client and task type (service)
			client = task.client
			service = task.service

			# Find existing PMO Assignment for the same client and service
			pmo_assignment = frappe.db.get_all(
				"PMO Assignment Details",
				filters={"client": client, "service_type": service},
				fields=["name", "total_actual_hour", "total_budget_hour"]
			)

			# If a PMO Assignment is found, update its total_actual_hour
			if pmo_assignment:
				pmo_assignment = frappe.get_doc("PMO Assignment Details", pmo_assignment[0].name)
				total_actual_hour = float(pmo_assignment.total_actual_hour or 0)

				# Add the actual_hours from the task to the total_actual_hour
				total_actual_hour += float(task.actual_hours or 0)

				# Update the PMO Assignment with the new total_actual_hour
				pmo_assignment.total_actual_hour = total_actual_hour
				pmo_assignment.variances_by_number = pmo_assignment.total_budget_hour - total_actual_hour
				pmo_assignment.flags.ignore_permissions = True
				pmo_assignment.flags.ignore_permissions = True
				pmo_assignment.flags.ignore_mandatory = True
				pmo_assignment.flags.ignore_links = True
				pmo_assignment.save()

				# Optionally, add a log or note for tracking
				frappe.msgprint(
					_("PMO Assignment for client {0} and service {1} updated. New total actual hours: {2}").format(
						client, service, total_actual_hour
					)
				)


@frappe.whitelist()
def get_clients(employee, client=None):
	filters = {}
	if client:
		filters = {"linked_service": client}
	service_budget_details = []
	service_budget_list = frappe.get_all("PMO Service Budget", filters=filters,
										 ignore_permissions=True, pluck="name")
	for service_budget in service_budget_list:
		doc = frappe.get_doc("PMO Service Budget", service_budget)
		for item in doc.audit_budget_table:
			if item.employee == employee:
				service_budget_details.append({
					"hour_no": item.hour_no,
					"employee": item.employee,
					"service_type": doc.service_type,
					"client": doc.linked_service
				})

	return service_budget_details
