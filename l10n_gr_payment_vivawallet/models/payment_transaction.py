# -*- coding: utf-8 -*-
# © 2018 bitwise.solutions <http://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.multi
    def vivawallet_s2s_do_transaction(self, response):
        return self._vivawallet_s2s_validate_tree(response)

    @api.multi
    def _vivawallet_s2s_validate_tree(self, response):
        self.ensure_one()
        if response.ok:
            self.write({
                'state': 'done',
                'date_validate': fields.Datetime.now(),
            })
            return True
        else:
            self.sudo().write({
                'state': 'error',
                'state_message': response.json().get('Message'),
                'date_validate': fields.Datetime.now(),
            })
            return False
