# -*- coding: utf-8 -*-
# © 2017 bitwise.solutions <http://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class TaxMechanismPrinter(models.Model):
    _name =  'tax.mechanism.printer'
    _description = 'Tax Mechanism printers'

    name = fields.Char()
    ip = fields.Char()
    port = fields.Integer()
    tax_mechanism_settings = fields.Many2one('tax.mechanism.setting')
