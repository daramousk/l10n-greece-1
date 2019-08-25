{
    'name': 'Account Payment VivaWallet',
    'version': '1.0',
    'license': 'AGPL-3',
    'author': "Odoo Community Association (OCA)",
    'website': '',
    'category': '',
    'depends': [
        'payment',
    ],
    'data': [
        'views/payment_vivawallet_templates.xml',
        'views/payment_acquirer.xml',
        'data/payment_icon.xml',
        'data/payment_acquirer.xml',
    ],
    'installable': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
}
