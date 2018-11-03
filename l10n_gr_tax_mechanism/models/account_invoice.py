# -*- coding: utf-8 -*-
# © 2017 bitwise.solutions <http://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import subprocess
from subprocess import Popen, PIPE, STDOUT
from odoo import api, exceptions, models, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def send_to_tax_mechanism(self):
        settings = self._get_tax_mechanism_settings()
        if not settings:
            raise exceptions.UserError(_('Activate your Tax mechanism first.'))
        for rec in self:
            p = Popen([
                'lpr',
                '-h',
                settings.tax_mechanism_printer_id.ip + 
                ':' + 
                settings.tax_mechanism_printer_id.port],
                stdout=PIPE,
                stdin=PIPE,
                stderr=STDOUT)
            response = p.communicate(input=self._get_data(
                rec, settings))[0]
# TODO verify that the data that is send is correct
# TODO test suits
            if p.responsecode != 0:
                raise exceptions.UserError(_(
                    'The following error occured while printing \n %s' % 
                    response))
            return True

    def _get_data(self, record, settings):
        """
        Get the fields that the user has set in settings and fetch them from
        the record.
        """
        data = ''
        for field in settings.tax_mechanism_field_ids:
            data.append(record.__getitem__(field.data.name))
            data.append(settings.separator)
        return data


    def _get_tax_mechanism_settings(self):
        return self.env['account.config.settings'] \
            .get_default_tax_mechanism_settings()
