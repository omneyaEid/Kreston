import frappe
from frappe import _


def get_data(data):
    data = {
        "fieldname": "linked_service",
        "non_standard_fieldnames": {
            "Lead": "linked_service",
        },
        "transactions": [
            {
                "label": _("Services Link"),
                "items": [
                    "Audit Service",
                    "Audit SP Service",
                    "Legal Cases Service",
                    "Special Report Service",
                    "SP M P Service",
                    "Other Service",
                ],
            },
            {
                "items": [
                    "Z Cases Service",
                    "ZDP SP Service",
                    "VAT Service",
                    "VAT Cases Service",
                    "AUP Service",
                ],
            },
            {
                "items": [
                    "LC Service",
                    "Zakat Service",
                    "Tax Service",
                    "SOM Service",
                    "VDP SP Service",
                ],
            },
        ],
    }

    # data.update({
    #     "fieldname": "linked_service",  # The fieldname could be used to store which services are selected
    # })

    return data
