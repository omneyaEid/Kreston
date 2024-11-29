frappe.ui.form.on("Daily TimeSheet", {
    day(frm) {
        var today = new Date();
        var currentMonth = today.getMonth();
        var currentYear = today.getFullYear();

        var selectedDay = frm.doc.day;

        if (selectedDay) {
            var selectedDate = new Date(selectedDay);
            var selectedMonth = selectedDate.getMonth();
            var selectedYear = selectedDate.getFullYear();

            // Check if the selected day is in the current month and year
            if (selectedMonth !== currentMonth || selectedYear !== currentYear) {
                frappe.msgprint(__('The selected day must be in the current month.'));
                frm.set_value('day', null);
            }
        }
    },
    employee(frm) {
        frm.fields_dict['tasks'].grid.get_field('client').get_query = null;

        if (frm.doc.employee) {
            frappe.call({
                method: 'kreston.kreston.doctype.daily_timesheet.daily_timesheet.get_clients',
                args: { employee: frm.doc.employee },
                callback: function (response) {
                    if (response.message && response.message.length > 0) {
                        var clients = Array.from(
                            new Set(
                                response.message.map(function (record) {
                                    return record.client;
                                })
                            )
                        );            
                        frm.fields_dict['tasks'].grid.get_field('client').get_query = function () {
                            return {
                                filters: {
                                    'name': ['in', clients]
                                }
                            };
                        };                        
                    } else {
                        frm.fields_dict['tasks'].grid.get_field('client').get_query = function () {
                            return {
                                filters: {
                                    'name': ['in', []]
                                }
                            };
                        };
                    }
                    frm.refresh_fields();
                }
            });
        }
    }
});


frappe.ui.form.on("Daily TimeSheet Details", {
    client: function (frm, cdt, cdn) {
        get_allowed_services(frm, cdt, cdn);
    },
    service: function (frm, cdt, cdn) {
        calculate_planned_hours(frm, cdt, cdn);
    },
    from_time: function (frm, cdt, cdn) {
        calculate_actual_hours(frm, cdt, cdn);
    },
    to_time: function (frm, cdt, cdn) {
        calculate_actual_hours(frm, cdt, cdn);
    }
});

function get_allowed_services(frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    if (frm.doc.employee && row.client) {
        frappe.call({
            method: "kreston.kreston.doctype.daily_timesheet.daily_timesheet.get_clients",
            args: {
                employee: frm.doc.employee,
                client: row.client
            },
            callback: function (response) {
                if (response.message && response.message.length > 0) {
                    var service_types = Array.from(
                        new Set(
                            response.message.map(function (record) {
                                return record.service_type;
                            })
                        )
                    );
                    frm.fields_dict.tasks.grid.update_docfield_property(
                        "service",
                        "options",
                        [""].concat(service_types)
                    );
                } else {
                    frm.fields_dict.tasks.grid.update_docfield_property(
                        "service",
                        "options",
                        [""].concat([])
                    );
                }
            }
        });
    }
}

function calculate_actual_hours(frm, cdt, cdn) {
    var row = locals[cdt][cdn];

    if (row.from_time && row.to_time) {
        var fromTime = moment(row.from_time, "HH:mm:ss");
        var toTime = moment(row.to_time, "HH:mm:ss");

        // Check if toTime is greater than fromTime
        if (toTime.isBefore(fromTime)) {
            row.actual_hours = 0;
        } else {
            // Calculate the difference in hours
            var duration = moment.duration(toTime.diff(fromTime));
            row.actual_hours = (duration.asMinutes() / 60).toFixed(2);
        }
        frm.refresh_field('tasks');
    }
}

function calculate_planned_hours(frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    if (frm.doc.employee && row.client && row.service) {
        frappe.call({
            method: "kreston.kreston.doctype.daily_timesheet.daily_timesheet.get_clients",
            args: {
                employee: frm.doc.employee,
                client: row.client
            },
            callback: function (response) {
                if (response.message && response.message.length > 0) {
                    // Filter records by selected service type
                    var service_records = response.message.filter(function (record) {
                        return record.service_type === row.service;
                    });

                    // Calculate the sum of hour_no for the given service type
                    var total_hours = service_records.reduce(function (sum, record) {
                        return sum + parseFloat(record.hour_no || 0);
                    }, 0);

                    row.planned_hours = total_hours;
                    frm.refresh_field('tasks');
                }
            }
        });
    }
}
