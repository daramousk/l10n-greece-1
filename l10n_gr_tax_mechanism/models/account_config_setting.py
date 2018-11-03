# -*- coding: utf-8 -*-
# © 2017 bitwise.solutions <http://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, exceptions, fields, models, _


class AccountConfigSettings(models.TransientModel):
    """
    This is the model that fetches and  shows the current settings.
    The actual settings are stored in tax.mechanism.settings
    """
    _inherit = 'account.config.settings'

    tax_mechanism_active = fields.Boolean()
    separator = fields.Char(size=1, default=';')
    tax_mechanism_field_ids = fields.Many2many(
        'tax.mechanism.field',
        string='Fields',
    )
    tax_mechanism_printer_id = fields.Many2one(
        'tax.mechanism.printer',
        string='Printer'
    )

    @api.multi
    def set_tax_mechanism_settings(self):
        tax_mechanism_settings_model = self.env['tax.mechanism.setting']
        if self.tax_mechanism_active:
            if not self.tax_mechanism_field_ids:
                raise exceptions.UserError(
                    _('Fill at least one field to be printed.'))
            result = tax_mechanism_settings_model.search([])
            if not result:
                tax_mechanism_settings_model.create({
                    'tax_mechanism_active': self.tax_mechanism_active,
                    'separator': self.separator,
                    'tax_mechanism_field_ids': [
                        (6, False, self.tax_mechanism_field_ids.ids)],
                    'tax_mechanism_printer_id': self.tax_mechanism_printer_id.id})
            else:
                result.write({
                    'tax_mechanism_active': self.tax_mechanism_active,
                    'separator':self.separator,
                    'tax_mechanism_field_ids': [
                        (6, False, self.tax_mechanism_field_ids.ids)],
                    'tax_mechanism_printer_id': self.tax_mechanism_printer_id.id})
        else:
            tax_mechanism_settings_model.search([]).unlink()
        return True

    @api.multi
    def get_default_tax_mechanism_settings(self, fields):
        tax_mechanism_settings_model = self.env['tax.mechanism.setting']
        result = tax_mechanism_settings_model.search([])
        if result:
            return {
                'tax_mechanism_active': result.tax_mechanism_active,
                'separator': result.separator,
                'tax_mechanism_field_ids': result.tax_mechanism_field_ids.ids,
                'tax_mechanism_printer_id': result.tax_mechanism_printer_id.id
                }
        return {}
