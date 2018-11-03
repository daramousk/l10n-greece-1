# -*- coding: utf-8 -*-
# © 2017 bitwise.solutions <http://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class TaxMechanismField(models.Model):
    _name = 'tax.mechanism.field'
    _description = 'Fields to be sent to the Tax Mechanism'

    name = fields.Char(string='Name', required=True)
    data = fields.Many2one(
        'ir.model.fields',
        domain=[('model', '=', 'account.invoice')])
    tax_mechanism_settings_id = fields.Many2one('tax.mechanism.setting')
