# -*- coding: utf-8 -*-
# Copyright 2019 bitwise.solutions <https://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from hashlib import sha1
from odoo import api, fields, models


class AccountInvoice(models.Model):
    inherit = 'account.invoice'

    sfs = fields.Char('')

    @api.depends(_get_fdss_fields)
    def _compute_fdss(self): # ΕΛΟΤ-928, ISO/IEC 8859-7
        # εκτός των πεδίων με αριθμό 1 και 2 του Πίνακα Α
        # delimiter #
        for rec in self:
            

    fdss = fields.Char(
        'Φορολογικά Δεδομένα Σήμανσης Στοιχείου',
        compute=_compute_fdss,
        store=True,
        help="Τα στοιχεια που αποστελλονται προς σημανση.")

    paips = fields.Char(
        "Προηγμενη Ηλεκτρονικη Υπογραφη (ΠΑΗΨΣ)"
        help="Αυτη η ακολουθια χαρακτηρων ειναι μοναδικη για καθε παραστατικο "
        "και υπολογιζεται κατα την εκτυπωση του. "
        "Χρεισιμοποιειται για να ικανοποιησει την Αυθεντικοτητα και "
        "ακεραιοτητα του περιεχομενου συμφωνα με Π.∆. 150/2001 Α' 125 "
        "",
    )

    def _save_sfs(self):
        """ Αρθρο 2. Δημιουργεια και αποθηκευση ΠΑΗΨΣ και ΣΦΣ.
        1) Λαβε τα ΦΔΣ απο την τοπικη βαση δεδομενων
        2) Χρησιμοποιησε την μοναδα tax_greece για να μετασχηματισεις τα 
        ΦΔΣ στην μορφη που περιγραφεται στο Π1 # TODO
        3) Στειλε τα μετασχηματισμενα ΦΔΣ στα σημεια που εχουν οριστει απο τον
        χρηστη.
        4) Λαβε τις ΣΦΣ και ΠΑΗΨΣ, αποθηκευσε την στο πεδιο sfs.
        """
        fds = self._get_fds() #1
        marked_data = self._mark_data() #2
        self.write({ #4
            'sfs': self._get_sfs(marked_data),
            'paips': self._get_paips(marked_data),
        })
   # πεδια header απο τον πινακα Α του παραρτηματος Π1
    versioning = fields.Char() # todo validation
    paips = fields.Char(
        'Ψηφιακό Ίχνος / Σήμανση - ΠΑΗΨΣ',
        help='Λαμβανεται απο τον Φορολογικο Μηχανισμο η αλλο παροχο.',
    ) # todo validation 80 = 77 + sp + 2digit Hex Sum
    language_code = fields.Char() # ISO 639-1
    currency_code = fields.Char() # ISO 4217 validation
    currency_name = fields.Char() # validation?
    document_type_code = fields.Selection() # get from GGPS validation
    document_name = fields.Char() # already existing?
    document_name_extra = fields.Char() # unneeded?
    document_invoice_type_code = fields.Selection([
        ('1', 'Τιμολόγηση'),
        ('2', 'Ανάθεση Τιμολόγησης'),
        ('3', 'Αυτοτιμολόγηση')],
    )

    @api.depends('document_invoice_type_code')
    def _compute_document_invoice_type_name(self):
        for rec in self:
            if rec.document_invoice_type_code == 1:
                rec.document_invoice_type_name = 'Τιμολόγιση'
                break
            elif rec.document_invoice_type_code == 2:
                rec.document_invoice_type_name = 'Ανάθεση Τιμολόγησης'
                break
            elif rec.document_invoice_type_code == 3:
                rec.document_invoice_type_name = 'Αυτοτιμολόγηση'
                break

    document_invoice_type_name = fields.Selection(
        compute='_compute_document_invoice_type_name',
        store=True,
    )

    @api.multi
    def _compute_document_print_spec(self):
        for rec in self:
            if self: # TODO the first time printed should print the first one
                rec.document_print_spec = 'Πρωτότυπο'
            else:
                rec.document_print_spec = 'Αντίτυπο'

    document_print_spec = fields.Char(compute='_compute_document_print_spec')
    document_invoice_queue = fields.Char(
        help='Συμπληρώνεται υποχρεωτικά εφόσον χρησιμοποιείται και έχει '
             'δηλωθεί στην αρμόδια ΔΟΥ') # TODO ?
    document_create_country_code = fields.Char() # TODO ISO 3166-1 alpha-2 check current company country
    document_create_county_code = fields.Char() #TODO code kalikratis Ν.3852/10
    document_create_county_name = fields.Char()
    document_create_state_name = fields.Char()
    document_create_city = fields.Char()
    # use GLN (Global Location Number)
    document_create_xlat = fields.Char('GEO x-lat')
    document_create_xlng = fields.Char('GEO x-lng')
    document_date_of_print = fields.Date() # TODO ΕΕΕΕΜΜΗΗ
    document_date_of_end = fields.Char() # TODO ΕΕΕΕΜΜΗΗ
    document_associated_docs = fields.Char() # TODO with comma all of them if any (eg. pickings, sales etc. MUST be seperated with comma


    # ΠΑΡΑΡΤΗΜΑ 2 ## ΣΤΟΙΧΕΙΑ ΕΚΔΟΤΗ - ΥΠΟΧΡΕΟΥ ΣΤΟ ΦΟΡΟ
    document_business_name = fields.Char()
    document_person_contact = fields.Char()
    document_business_code_from_client = fields.Char()
    document_business_vat = fields.Char()
    document_business_tax_office_code = fields.Char() # TODO GGPS
    document_business_tax_office_name = fields.Char()
    document_business_work_description = fields.Char() #TODO 1100330/1954/ΔΜ/ 6.10.08 (ΦΕΚ 2149/Β'/16.10.2008) «Καθορισμός Νέας Εθνικής Ονοματολογίας Οικονομικών Δραστηριοτήτων
    document_business_work_description_extra = field.Char()
    document_business_gemi = fields.Char() # TODO ΓΕΜΗ
    # should point to an external table, let them define as many as they want
    document_business_account_type = fields.Char() # GEMI
    document_business_account_number = fields.Char()
    document_business_country_code = fields.Char() # TODO  ISO 3166-1 alpha-2
    # for edra, use child ids here
    document_business_county_code = fields.Char() # kalicratis if greece
    document_business_county_name = fields.Char()
    document_business_state_name = fields.Char()
    document_business_city = fields.Char()
    document_business_street = fields.Char()
    document_business_street_no = fields.Char()
    document_business_geoxlat = fields.Float()
    document_business_geoxlng = fields.Float()
    document_business_zip = fields.Char() 
    document_business_tel = fields.Char()
    document_business_fax = fields.Char()
    document_business_email = fields.Char()
    document_business_url = fields.Char()
    document_business_extra_info = fields.Text()
    # for ypokatastimata should be as many as possible and should contain the
    # fields above 

    # C ΣΤΟΙΧΕΙΑ ΑΝΤΙΣΥΜΒΑΛΛΟΜΕΝΟΥ / ΑΓΟΡΑΣΤΗ
    document_buyer_company_name = fields.Char()
    document_buyer_company_contact = fields.Char()
    # add them in another model
    document_buyer_company_registry_code = fields.Char()
    document_buyer_company_registry_number = fields.Char()
    document_buyer_company_vat = fields.Char()
    document_buyer_company_tax_office_code = fields.Char() # GGPS
    document_buyer_company_tax_office_name = fields.Char()
    document_buyer_company_code_in_our_system = fields.Char()
    document_buyer_company_identity_type = fields.Char()
    document_buyer_company_identity_number = fields.Char()
    document_buyer_company_occupation = fields.Char() # there should be standards
    document_buyer_company_address_country = fields.Char() # iso 3166-1 alpha 2
    document_buyer_company_county_code = fields.Char() # Ν.3852/10)
    document_buyer_company_county_name = fields.Char()
    document_buyer_company_state_name = fields.Char()
    document_buyer_company_city = fields.Char()
    # here we see street fields, the fields are supposed to be printed in a specific way
    document_buyer_company_geoxlat = fields.Float() # geo
    document_buyer_company_geolng = fields.Float()
    # zip, tel, fax,email,url,
    document_buyer_company_extra_info = fields.Text()

    # D [Στοιχεία Διακίνησης] # only if we are sending something
    document_delivery_send_purpose = fields.Char()
    document_delivery_time_of_start = fields.Char()
    document_delivery_time_of_arrival = fields.Char()
    document_delivery_registration_number_of_first_vehicle = fields.Char()
    # da    Στοιχεία Δ/νσης - Τόπου Έναρξης της Αποστολής # TODO change below
    document_buyer_company_address_country = fields.Char() # iso 3166-1 alpha 2
    document_buyer_company_county_code = fields.Char() # Ν.3852/10)
    document_buyer_company_county_name = fields.Char()
    document_buyer_company_state_name = fields.Char()
    document_buyer_company_city = fields.Char()
    # here we see street fields, the fields are supposed to be printed in a specific way
    document_buyer_company_geoxlat = fields.Float() # geo
    document_buyer_company_geolng = fields.Float()
    # zip, tel, fax,email,url,
    document_buyer_company_extra_info = fields.Text()
    
    # Db [Στοιχεία Δ/νσης - Τόπου  # TODO change names below
    # Προορισμού της Αποστολής και παράδοσης των προϊόντων]
    document_buyer_company_address_country = fields.Char() # iso 3166-1 alpha 2
    document_buyer_company_county_code = fields.Char() # Ν.3852/10)
    document_buyer_company_county_name = fields.Char()
    document_buyer_company_state_name = fields.Char()
    document_buyer_company_city = fields.Char()
    # here we see street fields, the fields are supposed to be printed in a specific way
    document_buyer_company_geoxlat = fields.Float() # geo
    document_buyer_company_geolng = fields.Float()
    # zip, tel, fax,email,url,
    document_buyer_company_extra_info = fields.Text()
    
    # E [Στοιχεία παραλήπτη]
    document_business_name = fields.Char()
    document_person_contact = fields.Char()
    document_business_code_from_client = fields.Char()
    document_business_vat = fields.Char()
    document_business_tax_office_code = fields.Char() # TODO GGPS
    document_business_tax_office_name = fields.Char()
    document_business_work_description = fields.Char() #TODO 1100330/1954/ΔΜ/ 6.10.08 (ΦΕΚ 2149/Β'/16.10.2008) «Καθορισμός Νέας Εθνικής Ονοματολογίας Οικονομικών Δραστηριοτήτων
    document_buyer_company_address_country = fields.Char() # iso 3166-1 alpha 2
    document_buyer_company_county_code = fields.Char() # Ν.3852/10)
    document_buyer_company_county_name = fields.Char()
    document_buyer_company_state_name = fields.Char()
    document_buyer_company_city = fields.Char()
    # here we see street fields, the fields are supposed to be printed in a specific way
    document_buyer_company_geoxlat = fields.Float() # geo
    document_buyer_company_geolng = fields.Float()
    # zip, tel, fax,email,url,
    document_buyer_company_extra_info = fields.Text()
    # F [Στοιχεία Αναδόχου Τιμολόγησης] # if someone has been set
    external_invoicer_aggrement_description = fields.Char()
    external_invoicer_aggrement_number = fields.Char()
    external_invoicer_agreement_date = fields.Date()
    document_business_name = fields.Char()
    document_business_code_from_client = fields.Char()
    document_business_vat = fields.Char()
    document_business_tax_office_code = fields.Char() # TODO GGPS
    document_business_tax_office_name = fields.Char()
    document_business_work_description = fields.Char() #TODO 1100330/1954/ΔΜ/ 6.10.08 (ΦΕΚ 2149/Β'/16.10.2008) «Καθορισμός Νέας Εθνικής Ονοματολογίας Οικονομικών Δραστηριοτήτων
    document_buyer_company_address_country = fields.Char() # iso 3166-1 alpha 2
    document_buyer_company_county_code = fields.Char() # Ν.3852/10)
    document_buyer_company_county_name = fields.Char()
    document_buyer_company_state_name = fields.Char()
    document_buyer_company_city = fields.Char()
    # here we see street fields, the fields are supposed to be printed in a specific way
    document_buyer_company_geoxlat = fields.Float() # geo
    document_buyer_company_geolng = fields.Float()
    # zip, tel, fax,email,url,
    document_buyer_company_extra_info = fields.Text()

    # G [Στοιχεία Εντολέα]
    document_business_name = fields.Char()
    document_business_code_from_client = fields.Char()
    document_business_vat = fields.Char()
    document_business_tax_office_code = fields.Char() # TODO GGPS
    document_business_tax_office_name = fields.Char()
    document_business_work_description = fields.Char() #TODO 1100330/1954/ΔΜ/ 6.10.08 (ΦΕΚ 2149/Β'/16.10.2008) «Καθορισμός Νέας Εθνικής Ονοματολογίας Οικονομικών Δραστηριοτήτων
    document_buyer_company_address_country = fields.Char() # iso 3166-1 alpha 2
    document_buyer_company_county_code = fields.Char() # Ν.3852/10)
    document_buyer_company_county_name = fields.Char()
    document_buyer_company_state_name = fields.Char()
    document_buyer_company_city = fields.Char()
    # here we see street fields, the fields are supposed to be printed in a specific way
    document_buyer_company_geoxlat = fields.Float() # geo
    document_buyer_company_geolng = fields.Float()
    # zip, tel, fax,email,url,
    document_buyer_company_extra_info = fields.Text()
   
    # Ι [Λοιπές Συναλλακτικές Δαπάνες]
    # link to another model that allows us to add lots of them
    extra_costs_name = fields.Char()
    extra_costs_value = fields.Float()
    extra_costs_tax = fields.Float()
    extra_costs_tax_value = fields.Float()
    extra_costs_amount_total = fields.Float()

    extra_costs_full_before_tax_total = fields.Float()
    extra_costs_full_tax_amount_total = fields.Float()
    extra_costs_full_amount_total = fields.Float()
    
    # J [Λοιπές ειδικές επιβαρύνσεις - # link to model
    extra_withhold_amount = fields.Float()
    
    extra_withhold_all_total_amount = fields.Float()
    # another model with lots
    extra_withhold_tax_percentage = fields.Float()
    extra_withhold_amount_without_tax = fields.Float()
    extra_withhold_amount_with_tax = fields.Float()
    # these are sumations of the above
    extra_withhold_total_amount_without_tax = fields.Float()
    extra_withhold_discount_amount_total = fields.Float()
    extra_withhold_amount_total_after_discount = fields.Float()
    extra_withold_amount_without_tax_after_discount = fields.Float()
    extra_withhold_total_amount_including_tax = fields.Float()
    extra_withhold_total_amount_including_tax_local_currency = fields.Float()

    # L [Ανάλυση Ποσών Εκκαθάρισης - Προμήθειας]
    clean_total_amount_pre_tax = fields.Float()
    clean_total_tax_percentage = fields.Float()
    clean_total_tax_amount = fields.Float()
    clean_total_amount_total = fields.Float()
    # multiple record
    clean_total_tax_percentage = fields.Float()
    clean_total_tax_amount_pre_tax = fields.Float()
    clean_total_tax_amount = fields.Float()

    clean_total_tax_amount_pre_tax_total_vat_E = fields.Float()
    clean_total_tax_amount_pre_tax_after_discount = fields.Float()
    clean_total_tax_amount_total = fields.Float()

    # M [Γενικό Σύνολο & στοιχεία για πληρωμή]
    payment_previous_amount_total = fields.Float()
    payment_amount_prepaid = fields.Float()
    payment_amount_rounding = fields.Float()
    payment_amount_total = fields.Float()
    payment_payment_type_code = fields.Float()
    payment_date_to_pay = fields.Date() # EEEEMMHH
    payment_payment_reference_code = fields.Char()
    payment_payer_tin = fields.Char()
    payment_amount_of_goods = fields.Integer()
    payment_extra_payment_info = fields.Text()

    # N [Στοιχεία Τραπεζικών Lογαριασμών]
    issuer_bank_bic = fields.Char() # ISO 9362 BIC
    issuer_business_name = fields.Char()
    issuer_business_tin = fields.Char()
    issuer_business_tax_office_code = fields.Char() # ggps
    issuer_business_tax_office_name = fields.Char()
    issuer_business_bank_code = fields.Char()
    issuer_business_bank_name = fields.Char()
    issuer_business_iban = fields.Char() # take it from
    issuer_business_account_extra_info = fields.Text()
    # στοιχεια αγοραστη
    buyer_bank_bic = fields.Char() # ISO 9362 BIC
    buyer_business_name = fields.Char()
    buyer_business_tin = fields.Char()
    buyer_business_tax_office_code = fields.Char() # ggps
    buyer_business_tax_office_name = fields.Char()
    buyer_business_bank_code = fields.Char()
    buyer_business_bank_name = fields.Char()
    buyer_business_iban = fields.Char() # take it from
    buyer_business_account_extra_info = fields.Text()
 
    # [Στοιχεία Σύμβασης - Εκτέλεσης παραγγελίας - Χρηματοδότησης]
    contract_type_code = fields.Char()
    contract_description = fields.Char()
    contract_number = fields.Char()
    contract_date = fields.Date() # EEEEMMHH
    contract_number_ada = fields.Integer()
    contract_kae = fields.Char() # comma seperated
    contract_kay = fields.Char() # comma seperated
    contract_order = fields.Char() # comma seperated
    contract_ops_mis = fields.Char() # maybe validate online?
    contract_sae_code = fields.Char()
    contract_sae_year = fields.Char() # year EEEE
    contract_sae_enarithmos = fields.Char() # Κωδικός Εναρίθμου Έργου

    # P [Λοιπά Στοιχεία & Ενδείξεις]
    document_extra_info = fields.Text()
    document_observations_comments = fields.Text()
