frappe.listview_settings['Grey Area'] = {
    onload : function (listview) {
        // add button to menu
        listview.page.add_action_item(__("Move To Pipline Content"), function () {
            moveToLead(listview);
        });
    }
}


function moveToLead(listview) {
    let names = [];
    $.each(listview.get_checked_items(), function (key, value) {
        names.push(value.name);
    });

    if (names.length === 0) {
        frappe.throw(__("No rows selected."));
    }

    // Call the server-side method to move the leads
    frappe.call({
        method: "kreston.methods.grey_area.move_from_grey_area",
        args: {
            grey_area_names: names
        },
        callback: function (response) {
            if (response.message) {
                frappe.msgprint(response.message);
                listview.refresh(); // Refresh the listview after moving leads
            }
        },
    });
}
