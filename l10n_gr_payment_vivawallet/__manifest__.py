# -*- coding: utf-8 -*-
# © 2018 bitwise.solutions <http://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Payment VivaWallet',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': "bitwise.solutions,Odoo Community Association (OCA)",
    'website': 'http://bitwise.solutions',
    'category': 'Banking addons',
    'depends': [
        'payment',
    ],
    'data': [
        'views/payment_vivawallet_templates.xml',
        'views/payment_acquirer.xml',
        'data/payment_acquirer.xml',
    ],
    'installable': True,
}
