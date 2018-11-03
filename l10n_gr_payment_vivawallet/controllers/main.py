# -*- coding: utf-8 -*-
# © 2018 bitwise.solutions <http://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import requests
from odoo import http
from odoo.http import request
from werkzeug.exceptions import BadRequest
from odoo.addons.website_sale.controllers.main import WebsiteSale


class Vivawallet(http.Controller):

    @http.route(
        ['/payment/vivawallet/create_charge'],
        type='http',
        auth='public',
        website=True)
    def vivawallet_create_charge(self, **post):
        token = post.get('vivaWalletToken')
        baseurl = post.get('vivawallet_baseurl')
        if not token or not baseurl:
            raise BadRequest
        response = requests.post(
            '%s/api/transactions' % baseurl, params={'PaymentToken': token})
        website_sale = WebsiteSale()
        website_sale.payment_transaction(int(post['acquirer_id']))
        request.website.sale_get_transaction().vivawallet_s2s_do_transaction(response)
        return request.redirect('/shop/payment/validate')
