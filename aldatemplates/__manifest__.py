# Copyright 2020 CommitSun (<http://www.commitsun.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "PMS Alda Hotels",
    "version": "14.0.2.0.1",
    "author": "Commit [Sun], Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": True,
    "category": "pms",
    "website": "https://github.com/OCA/aldahotels",
    "depends": [
        "pms",
    ],
    "data": [
        "data/confirmation_template.xml",
        "security/ir.model.access.csv",
        "views/pms_property_views.xml",
    ],
    "installable": True,
}