# -*- coding: utf-8 -*-
# © 2018 bitwise.solutions <http://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "l10n_gr_tax_mechanism",
    "version": "10.0.1.0.0",
    "author": "bitwise.solutions,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "",
    "summary": "",
    "depends": [
        "base",
        "account_accountant",
        "account",
    ],
    "data": [
        'views/account_config_settings.xml',
        'views/tax_mechanism_printer.xml',
        'views/account_invoice.xml',
    ],
    "installable": True,
    "application": False,
}
