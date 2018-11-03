# -*- coding: utf-8 -*-
# © 2017 bitwise.solutions <http://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class TaxMechanismSettings(models.Model):
    _name = 'tax.mechanism.setting'
    _description = 'Tax Mechanism settings'

    tax_mechanism_active = fields.Boolean()
    separator = fields.Char(size=1, default=';')
    tax_mechanism_field_ids = fields.Many2many(
        'tax.mechanism.field',
        string='Fields',
    )
    tax_mechanism_printer_id = fields.Many2one(
        'tax.mechanism.printer',
        string='Printer',
    )
