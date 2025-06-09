# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, _


class srPropertyPartialPayment(models.Model):
    _name = 'sr.property.partial.payment'
    _description = 'Property Partial Payment'

    name = fields.Char('Name', required=True)
    number_of_installments = fields.Integer("No of Installments", required=True)


class srPropertyType(models.Model):
    _name = 'sr.property.type'
    _description = 'Property Type'

    name = fields.Char('Name', required=True)


class srPropertyInterior(models.Model):
    _name = 'sr.property.interior'
    _description = 'Property Interior'

    name = fields.Char('Name', required=True)


class srPropertyExterior(models.Model):
    _name = 'sr.property.exterior'
    _description = 'Property Exterior'

    name = fields.Char('Name', required=True)


class srPropertyFacade(models.Model):
    _name = 'sr.property.facade'
    _description = 'Property Facede'

    name = fields.Char('Name', required=True)


class srPropertyAmenities(models.Model):
    _name = 'sr.property.amenities'
    _description = 'Property Amenities'

    name = fields.Char('Name', required=True)


class srPropertyNeighborhood(models.Model):
    _name = 'sr.property.neighborhood'
    _description = 'Property Neighborhood'

    name = fields.Char('Name', required=True)


class srPropertyTransportation(models.Model):
    _name = 'sr.property.transportation'
    _description = 'Property Transportation'

    name = fields.Char('Name', required=True)


class srPropertyLandscape(models.Model):
    _name = 'sr.property.landscape'
    _description = 'Property Landscape'

    name = fields.Char('Name', required=True)
