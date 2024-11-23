// Copyright (c) 2024, omneyaeid827@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Cut off"] = {
	"filters": [
		{
			"fieldname":"from_year",
			"label": __("From Year"),
			"fieldtype": "Select",
			"options": get_years(),
			"default": 2019,
			"reqd": 1
		},
		{
			"fieldname":"to_year",
			"label": __("To Year"),
			"fieldtype": "Select",
			"options": get_years(),
			"default": new Date().getFullYear() + 1,
			"reqd": 1
		}
	]
};


function get_years() {
    let years = [];
    for (let i = 2019; i <= new Date().getFullYear() + 3; i++) {
        years.push(i);
    }
    return years;
}