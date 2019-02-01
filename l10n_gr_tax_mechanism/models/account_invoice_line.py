# -*- coding: utf-8 -*-
# Copyright 2019 bitwise.solutions <https://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    """ Περιεχει τα πεδια που οριζονται απο τον Πινακα 2 του παραρτηματος Π1.
    TODO: Επειδη δεν ειναι ξεκαθαρο ποια πεδια ειναι υποχρεωτικα και ποια οχι,
    ολα ειναι υποχρεωτικα για την ωρα
    TODO: Πρεπει να τοποθετηθουν τα πεδια και στα αλλες γραμμες παραστατικων
    TODO: Καποια πεδια ηδη παρεχονται, να συγχωνευθουν
    """
    _inherit = 'account.invoice.line'

    date = fields.Date(
        string='Ημερομηνια',
        help='Αφορά Στοιχεία Αξίας. Συμπληρώνεται μόνον στη Τιμολόγηση '
             'Επαναλαμβανομένων Πωλήσεων',
    )# TODO prepei na apothikeyetai se morfi ΕΕΕΕΜΜΗΗ
    product_code_by_provider = fields.Char(
        string='Κωδικος Ειδους.',
        help='Κωδικοποιηση ειδους κατα εκδοτη.',
    )
    product_code_cpv = fields.Char(
        'Κωδικος Ειδους CPV',
        # TODO use this??
        # http://github.com/uktrade/dit-classification-matcher/tree/master/files
        # make the codes to xml and save them on another module
        help='Υποχρεωτική στην περίπτωση '
             'τιμολογίου προς το Δημόσιο.',
    )
    product_code_common = fields.Char(
        'Κωδικοποίηση Είδους',
        help='Κοινη Κωδικοποιηση (ΕΑΝ η ΤΙΝ')
    product_code_family = fields.Char('Κωδικος Οικογενιας κατηγοριας ειδους.')
    product_code_country_from = fields.Char() # TODO ISO 3166-1 alpha-2
    product_code_taric = fields.Char() # TODO https://en.wikipedia.org/wiki/TARIC_code
    product_type_description = fields.Char(
        'Ειδος/περιγραφη αγαθου',
        related='name',
    )
    product_colour = fields.Char()
    product_size = fields.Char()
    line_order_code = fields.Char(
        'Κωδικος Παραγγελιας',
        related='invoice_id.number',
    )
    line_shipment_code = fields.Char(
        'Κωδικος Μεταφορας/Αποστολης/Παρτιδας',
    )
    line_date_lifespan = fields.Datetime(
        'Προσδιορισμος Χρονικης διαρκειας ζωης της παρτιδας',
        help='Ημερομηνια ληξης του προιοντος (εαν υπαρχει) ως προεπιλογη',
    )
    line_code_delivery = fields.Char(
        'Κωδικος Παραδοσης',
        help='Βοηθητικος κωδικος παραδοσης',
    )
    line_date_begin_service = fields.Date(
        'Ημερομηνια Εναρξης περιοδου παροχης υπηρεσιας',
    ) # TODO ΕΕΕΕΜΜΗΗ
    line_date_end_service = fields.Date(
        'Ημερομηνια Ληξης περιοδου παροχης υπηρεσιας.',
    ) #ΤΟΔΟ ΕΕΕΕΜΜΗΗ
    line_quantity_unit_code = fields.Char(
        'Κωδικος Μοναδας μετρησης της ποσοτητας (Συμφωνα με SI)',
    )
    line_quantity_unit_name = fields.Char(
        'Ονομασια Μοναδας μετρησης (Συμφωνα με SI)',
    )
    line_price_cost = fields.Float(
        'Τιμη Κοστους',
        'Αφορά Στοιχεία Αξίας. Συμπληρώνεται μόνον στην περίπτωση εφαρμογής '
        'ειδικού καθεστώτος ΦΠΑ (Περιθώριο Κέρδους.)',
    )
    line_price_unit = fields.Float('Τιμη πωλησης μοναδας')
    line_previous_remaining_quantity = fields.Float(
        'Προηγ. Υπόλοιπο Ποσότητας (Κύριας Μονάδας Μέτρησης)',
        help='Αφορά Στοιχεία Αξίας. Συμπληρώνεται '
             'μόνο στην περίπτωση Εκκαθαρίσεων',
    )
    line_quantity_received = fields.Float('Ποσοτητα Παραλειφθεντων')
    line_quantity_sold = fields.Float('Ποσοτητα Πωληθεντων')
    line_quantity_new_stock = fields.Float('Νεο υπολοιπο ποσοτητας')
    line_quantity = fields.Float('Ποσοτητα σε αριθμο')
    line_quantity_unit_code = fields.Char(
        'Κωδικος μοναδας μετρησης ποσοτητας συμφωνα με το SI',
    )
    line_quantity_unit_name = fields.Char(
        'Ονομασια μοναδας μετρησης ποσοτητας συμφωνα με το SI',
    )
    line_quantity_alternative = fields.Float(
        'Ποσότητα με βάση την εναλλακτική μονάδα μέτρησης',
    )
    line_special_taxes = fields.Many2one(
        'Λοιπες ειδικες φορολογικες επιβαρυνσεις',
    )
    line_special_taxes_description = fields.Char(
        'Περιγραφη επιβαρυνσης / παρακρατησης',
        help='Συμπληρώνεται υποχρεωτικά εφ’ όσον '
             'επιβάλλεται τέτοια επιβάρυνση (ή '
             'παρακράτηση) και δεν έχει ήδη '
             'συνυπολογισθεί - συμπεριληφθεί στην '
             'τελική τιμή. ',
    ) # τοδο βαλτο στο μοντελο του
    line_special_taxes_amount_total = fields.Float(
        'Συνολικο αρθροιστικο ποσο.',
    )
    line_cost_amount_total = fields.Float(
        'Συνολικη Αξια Κοστους',
        help='Αφορά Στοιχεία Αξίας. Συμπληρώνεται μόνον στην περίπτωση '
             'εφαρμογής ειδικού καθεστώτος ΦΠΑ (Περιθώριο Κέρδους)',
    )
    line_value_total_amount_before_discount = fields.Float(
        'Συνολικη Καθαρη Αξια Ειδων Προ Εκπτωσης',
        help='Αφορα Στοιχεια Αξιας',
    )
    line_percentage_discount_or_surcharge = fields.Float(
        'Ποσοστο Εκπτωσης η προσαυξησης',
        help='Αρνητικη τιμη για εκπτωση, θετικη για προσαυξηση',
    )
    line_total_taxable_value_of_sale_after_discount_without_vat = fields.Float(
        'Καθαρή Συνολική φορολογητέα Αξία Πώλησης χωρίς ΦΠΑ μετά την Έκπτωση',
        help='Αφορα στοιχεια αξιας',
    )
    line_difference_amount_profit = fields.Float(
        'Διαφορα - Περιθωριο Κερδους',
        help='Αφορά Στοιχεία Αξίας. Συμπληρώνεται μόνον στην περίπτωση '
             'εφαρμογής ειδικού καθεστώτος ΦΠΑ (Περιθώριο Κέρδους)',
    )
    line_tax_percentage = fields.Float('Συντελεστης ΦΠΑ')
    line_tax_amount = fields.Float(
        'Συνολικο ποσο ΦΠΑ που αντιστοιχει',
        help='Αφορα Στοιχεια Αξιας',
    )
    line_tax_amount_total_with_vat = fields.Float(
        'Συνολικο ποσο με ΦΠΑ',
        help='Αφορα Στοιχεια Αξιας',
    )
    line_observations_comments = fields.Text(
        'Παρατηρησεις - Σχολια',
        help='Επισημαίνεται ότι μπορεί να γίνεται χρήση για την αναγραφή '
             'ενδείξεων που επιβάλλονται από άλλες διατάξεις',
    )
    # μονο για Συγκεντρωτικες φορτωτικες μεχρι το τελος
    line_receiver_company_name = fields.Char(
        'Επωνυμια επιχειρησης παραλειπτη',
        help='Συμπληρώνεται στις περιπτώσεις Συγκεντρωτικών Φορτωτικών',
    )
    line_receiver_company_vat = fields.Char('ΑΦΜ παραληπτη')
    line_receiver_company_tax_office_code = fields.Char('Κωδικος Δ.Ο.Υ')
    line_receiver_company_tax_office_name = fields.Char('Ονομασια Δ.Ο.Υ')
    line_receiver_company_job = fields.Char()
    line_receiver_country_code = fields.Char()#todo standardize
    line_receiver_demos_code = fields.Char() # todo standardize
    line_receiver_demos_name = fields.Char() # todo standardize
    line_receiver_state_name = fields.Char() # todo standardize
    line_receiver_city = fields.Char() # todo standardize
    line_receiver_street = fields.Char() # todo standardize with comma
    line_receiver_street_no = fields.Integer() # todo standardize
    # GEO x-lat xx, GEO x-lng yy
    line_receiver_geo_x_lat = fields.Float() # todo standardize
    line_receiver_geo_x_lng = fields.Float() # todo standarzize
    line_receiver_zip = fields.Char() # todo standardize
    line_receiver_tel = fields.Integer() # todo standardize
    line_receiver_fax = fields.Integer() # todo standardize
    line_receiver_email = fields.Char() # todo standardize
    line_receiver_info = fields.Text('Λοιπές Πληροφορίες')
    # TODO when there is a specific encoding requested, save the information in
    # its default format and when printing/showing it, then transform
    # (if that kind of data already exists (ie. Countries)

