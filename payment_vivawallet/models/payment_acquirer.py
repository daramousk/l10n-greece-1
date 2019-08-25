# -*- coding: utf-8 -*-
# © 2018 bitwise.solutions <http://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

BASEURL_TEST = 'https://demo.vivapayments.com'
BASEURL_PRODUCTION = 'https://www.vivapayments.com'


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('vivawallet', 'Viva Wallet')])
    vivawallet_public_key = fields.Char(
        required_if_provider='vivawallet',
        string='Public Key',
    )

    @api.multi
    @api.depends('environment')
    def _compute_vivawallet_baseurl(self):
        for rec in self:
            if rec.environment == 'test':
                rec.vivawallet_baseurl = BASEURL_TEST
            else:
                rec.vivawallet_baseurl = BASEURL_PRODUCTION

    vivawallet_baseurl = fields.Char(
        required_if_provider='vivawallet',
        compute='_compute_vivawallet_baseurl',
        store=True,
    )

    @api.multi
    def vivawallet_form_generate_values(self, values=None):
        self.ensure_one()
        # currently supports en, el, ro. Probably ISO 639-1 but
        # the documentation does not specify.
        # Also, Odoo uses a different format.
        # Let's default to English for now just to be safe.
        lang = 'en'
        values.update({
            'public_key': self.vivawallet_public_key,
            'amount': int(values.get('amount', 0) * 100),
            'lang': lang,
            'baseurl': self.vivawallet_baseurl,
        })
        return values
