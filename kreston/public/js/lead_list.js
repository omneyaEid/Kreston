// Copyright (c) 2024, omneyaeid827@gmail.com and contributors
// For license information, please see license.txt

frappe.listview_settings['Lead'].onload = function (listview) {
    // add button to menu
    listview.page.add_action_item(__("Move To Grey Area"), function () {
        moveToGreyArea(listview);
    });
};

function moveToGreyArea(listview) {
    let names = [];
    $.each(listview.get_checked_items(), function (key, value) {
        names.push(value.name);
    });

    if (names.length === 0) {
        frappe.throw(__("No rows selected."));
    }

    // Call the server-side method to move the leads
    frappe.call({
        method: "kreston.methods.lead.move_to_grey_area",
        args: {
            lead_names: names
        },
        callback: function (response) {
            if (response.message) {
                frappe.msgprint(response.message);
                listview.refresh(); // Refresh the listview after moving leads
            }
        },
    });
}
