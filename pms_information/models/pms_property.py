# Copyright 2024 OsoTranquilo - José Luis Algara
# Copyright 2024 Irlui Ramírez
# From Consultores Hoteleros Integrales (ALDA Hotels) - 2024
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class PmsProperty(models.Model):
    _inherit = "pms.property"

    total_rooms = fields.Integer(
        string='Total rooms', 
        compute='_compute_total_rooms'
    )

    company_vat = fields.Char(
        string='NIF', 
        compute='_compute_company_vat'
    )

    email= fields.Char(
        string='Email Hotel', 
        compute='_compute_email'
    )

    bank= fields.Char(
        string='Bank', 
        compute='_compute_swift'
    )

    acc_number= fields.Char(
        string='Account Bank', 
        compute='_compute_swift'
    )
    swift= fields.Char(
        string='Swift', 
        compute='_compute_swift'
    )

    total_tourism_rooms = fields.Integer(
        string='Tourism Rooms',
    )

    open_date = fields.Datetime(
        string='Open date',
        default=fields.Datetime.now,
    )

    is_ramp_up = fields.Boolean(
        string='Ramp-Up', 
        compute='_compute_state', 
        default=True,
    )
    
    is_ramp_rate = fields.Boolean(
        string='Ramp-Rate', 
        compute='_compute_state',
        default=False,
    )

    months_to_ramp_rate = fields.Integer(
        string='Month to Ramp-Rate', 
        compute='_compute_months_to_ramp_rate'
    )

    months_open = fields.Integer(
        string='Months Open',
        compute='_compute_months_open',
    )

    @api.depends('open_date')
    def _compute_months_open(self):
        for record in self:
            if record.open_date:
                open_date = fields.Datetime.from_string(record.open_date)
                today = datetime.now()
                diff_months = (today.year - open_date.year) * 12 + today.month - open_date.month
                record.months_open = diff_months
            else:
                record.months_open = 0

    @api.depends('open_date')
    def _compute_total_rooms(self):
        for record in self:
            target_rooms = (
                self.env["pms.room"]
                .with_context(active_test=True)
                .sudo().search([("pms_property_id", "=", record.id)])
            )
            record.total_rooms = len(target_rooms)
    
    @api.depends('partner_id', 'partner_id.email')
    def _compute_email(self):
        for record in self:
            if record.partner_id and record.partner_id.email:
                record.email = record.partner_id.email
            else:
                record.email = "no asignado"

    @api.depends('company_id', 'company_id.vat')
    def _compute_company_vat(self):
        for record in self:
            if record.company_id and record.company_id.vat:
                record.company_vat = record.company_id.vat
            else:
                record.company_vat = "no asignado"

    @api.depends('partner_id', 'partner_id.bank_ids')
    def _compute_swift(self):
        for record in self:
            if record.partner_id and record.partner_id.bank_ids:
                record.swift = record.partner_id.bank_ids[0].bank_id.bic
                record.bank = record.partner_id.bank_ids[0].bank_id.name
                record.acc_number= record.partner_id.bank_ids[0].acc_number
            else:
                record.swift = "no asignado"
                record.bank = "no asignado"
                record.acc_number = "no asignado"

    @api.constrains('total_tourism_rooms')
    def _check_total_tourism_rooms(self):
        for record in self:
            if record.total_tourism_rooms > record.total_rooms:
                raise ValidationError(
                    'The number of tourist rooms cannot exceed the total number of rooms.'
                )

    @api.depends('open_date')
    def _compute_state(self):
        for record in self:
            if record.open_date:
                open_date = fields.Date.from_string(record.open_date)
                today = fields.Date.context_today(self)
                #today = fields.Date.today()
                diff_months = (today.year - open_date.year) * 12 + today.month - open_date.month
                record.is_ramp_up = diff_months < 17
                record.is_ramp_rate = diff_months >= 17
            else:
                record.is_ramp_up = False
                record.is_ramp_rate = False
    
    @api.depends('open_date')
    def _compute_months_to_ramp_rate(self):
        for record in self:
            if record.open_date:
                open_date = fields.Date.from_string(record.open_date)
                today = fields.Date.context_today(self)
                diff_months = (today.year - open_date.year) * 12 + today.month - open_date.month
                if diff_months < 17:
                    record.months_to_ramp_rate = 17 - diff_months
                else:
                    record.months_to_ramp_rate = 0
            else:
                record.months_to_ramp_rate = 0