# -*- coding: utf-8 -*-
# Copyright 2019 bitwise.solutions <https://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

# σταθερα πεδια και συνολικα δεδομενα, του εκαστοτε φορολογικου στοιχειου.
HEADER_FIELDS = {'':[]} # maybe move this to data/*? no?
# πεδια που αφορουν καθε ενα απο τα αγαθα του εκαστοτε φορολογικου στοιχειου
DETAIL_FIELDS = {'':[]}

# Ο Κ.Φ.Α.Σ μας δινει εναν Πινακα Φορολογικων Στοιχειων, η μεταβλητη
# REQUIRED_MODELS περιεχει τα μοντελα του Odoo που αντιστοιχουν σε αυτα
REQUIRED_MODELS = ['account.invoice', 'account.payment', 'stock.picking']

REQUIRED_FIELDS = {
    'account.invoice': ['number', 'date_invoice'],
    'account.payment': [],
    'stock.picking': [],
    }


class AccountConfigSettings(models.TransientModel):
    _name = 'account.config.settings'
    _inherit = 'res.config.settings'

    def _get_required_models(self):
        """ Συμφωνα με τον Κ.Φ.Α.Σ τα φορολογικα στοιχεια ειναι τα ακολουθα:
        (στα δεξια το μοντελο που αντιστοιχει)
        ΤΙΜΟΛΟΓΙΟ ΠΩΛΗΣΗΣ               -> account.invoice -> Invoices
        ΤΙΜΟΛΟΓΙΟ ΠΑΡΟΧΗΣ ΥΠΗΡΕΣΙΩΝ     -> account.invoice -> Invoices
        ΤΙΜΟΛΟΓΙΟ ΑΓΟΡΑΣ                -> account.invoice -> Invoices
        ΠΙΣΤΩΤΙΚΟ ΤΙΜΟΛΟΓΙΟ             -> account.payment -> ?
        ΔΕΛΤΙΟ ΑΠΟΣΤΟΛΗΣ                -> stock.picking -> Delivery Slip
        ΣΥΓΚΕΝΤΡΩΤΙΚΟ ΔΕΛΤΙΟ ΑΠΟΣΤΟΛΗΣ  -> καταργηθηκε
        ΕΚΚΑΘΑΡΙΣΗ                      -> ?
        ΑΠΟΔΕΙΞΗ ΛΙΑΝΙΚΗΣ ΣΥΝΑΛΛΑΓΗΣ    -> account.invoice
        ΑΠΟΔΕΙΞΗ ΕΠΙΣΤΡΟΦΗΣ             -> stock.picking
        ΦΟΡΤΩΤΙΚΗ                       -> καταργηθηκε
        ΣΥΓΚΕΝΤΡΩΤΙΚΗ ΦΟΡΤΩΤΙΚΗ         -> καταργηθηκε
        ΑΠΟΔΕΙΞΗ ΜΕΤΑΦΟΡΑΣ ΑΠΟΣΚΕΥΩΝ    -> account.invoice
        ΔΙΟΡΘΩΤΙΚΟ ΣΗΜΕΙΩΜΑ ΜΕΤΑΦΟΡΑΣ   -> account.invoice
        ΑΠΟΔΕΙΞΗ ΑΥΤΟΠΑΡΑΔΟΣΗΣ          -> account.invoice
        ΑΠΟΔΕΙΞΗ ΔΑΠΑΝΗΣ                -> account.invoice
        """
        return self.env['ir.model'].search([('model', 'in', REQUIRED_MODELS)])

    models_to_send = fields.Many2many(
        'ir.model',
        help='Παραστατικα που θα αποσταλλουν',
        default=_get_required_models,
    )

    def _get_required_fields(self):
        """ Τα Φορολογικα Στοιχεια για να οριζονται ως φορολογικα στοιχεια
        πρεπει να περιεχουν συγκεκριμενα πεδια.
        Αυτα τα πεδια προεπιλεγονται για αποστολη.
        """
        fields_model = self.env['ir.model.fields']
        fields = fields_model
        fields += fields_model.search([
            ('model', 'in' REQUIRED_FIELDS.keys()),
            ('name', 'in', REQUIRED_FIELDS.values()),
        ])
        return fields

    fields_to_send = fields.Many2many(
        'ir.model.fields',
        help='Πεδια των παραπανω παραστατικων που θα αποσταλλουν.',
        default=_get_required_fields,
    )
    servers = fields.Many2many(
        'account.tax.servers',
        help='Εξυπηρετες που θα επικοινωνουν με το Odoo '
             'και ο λογος επικοινωνιας',
    )

    def _send_fdss(self):
        """ Αρθρο 7 ΔΙΑΒΙΒΑΣΗ ΦΟΡΟΛΟΓΙΚΩΝ ΣΤΟΙΧΕΙΩΝ
            Εδω γινεται συλλογη των στοιχειων και αποστολη τους σε
            απομακρυσμενους εξυπηρετες.
            * Αυτη η λειτουργια μπορει εναλλακτικα να επιτελειται απο τον
            Φορολογικο Μηχανισμο.
            Τα παρακατω στοιχεια στελνονται ΥΠΟΧΡΕΩΤΙΚΑ και ονομαζονται ΦΔΣΣ.
            1) Τα ΦΔΣ τα οποια εχουν σημανθει με συμφωνα με το Π1
            2) Τον Ημερησιο Αυξοντα Αριθμο του φορολογικου στοιχειου
            3) Τον Γενικο Αυξοντα Αριθμο του φορολογικου στοιχειου
            4) Την Χρονοσφραγιδα Σημανσης του φορολογικου στοιχειου
            5) Εαν η σημανση γινεται απο Φορολογικο Μηχανισμο, τοτε στελνουμε
            τον αριθμο μητρωου του. Εαν η σημανση γινεται απο αυλα μεσω ΠΑΦΣ
            τοτε στελνουμε τον Μοναδικο Αριθμο μητρωου του Υποχρεου.

            Τα 2, 3, 4 ειναι αποθηκευμενα στο παραστατικο και εχουν ληφθει ειτε
            απο τον φορολογικο μηχανισμο ειτε απο ΠΑΦΣ.

            Η κωδικοποιηση της αλληλουχιας ΦΔΣΣ γινεται με το προτυπο ΕΛΟΤ-928
        """

    def _get_daily_paips(self):
        """ Αρθρο 5. ΔΗΜΙΟΥΡΓΙΑ ΚΑΙ ΑΠΟΘΗΚΕΥΣΗ ΓΕΝΙΚΗΣ ΗΜΕΡΗΣΙΑΣ ΠΑΗΨΣ
        1) Λαβε την Γενική Ημερήσια ΠΑΗΨΣ καθως και τον χρονο δημιουργειας της
        (ΕΕΜΜΗΗΛΛΩΩ) απο το συστημα που εχει οριστει (ethernet η usb)
        απο τον χρηστη.
        2) Αποθηκευσε την Γενικη Ημερησια ΠΑΗΨΣ και συνδεσε την με ολες τις
        ΠΑΗΨΣ που περιεχει. (account.daily.paips)
        """
