import frappe
from frappe import _


def get_data(data):
    data = {
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

    data.update({"fieldname": "linked_service"})

    return data
