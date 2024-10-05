// Copyright (c) 2024, omneyaeid827@gmail.com and contributors
// For license information, please see license.txt

// Function to update heading color based on custom_audit field
function updateHeadingColor(frm) {
    const custom_audit = frm.doc.custom_audit; // Replace with your actual field name

    // Get the heading element and set its color based on custom_audit field
    const heading = document.querySelector('[data-fieldname="custom_to_be_consider_in_quaem"] h4');
    
    if (heading) {
        if (custom_audit) {
            heading.style.color = "red"; // Change color to red if custom_audit is active
        } else {
            heading.style.color = ""; // Reset color if custom_audit is not active
        }
    }
}