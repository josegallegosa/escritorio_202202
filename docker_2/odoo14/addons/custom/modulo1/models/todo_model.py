# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cliente(models.Model):
    _name = 'cliente'
    name = fields.Char('Nombres', required=False)
    
    last_name = fields.Char('Apellidos', required=False)

    type_identification = fields.Many2one('l10n_latam.identification.type',
        string="Tipo Documento Identificacion", index=True, auto_join=True,default=5)
    
    num_identification = fields.Char(string='Numero de documento', help="Identification Number for selected type")

    sexo = fields.Selection(
        string="Sexo",
        selection=[
            ('masculino', 'Masculino'),
            ('femenino', 'Femenino'),
            ('otros', 'Otros'),
        ], default="masculino"
    )

    tipo_empresa = fields.Selection(
        string="TipoEmpresa",
        selection=[
            ('clinica', 'Clinica'),
            ('hotel', 'Hotel'),
            ('restaurant', 'Restaurant'),
            ('colegio', 'Colegio'),
            ('universidad', 'Universidad'),
            ('supermercado', 'Supermercado'),
            ('otros', 'Otros'),
        ], default="hotel"
    )

    direccion = fields.Char('Direccion', required=False)

    date_order = fields.Datetime(string='Fecha Afiliación', readonly=False, index=True, default=fields.Datetime.now)

    phone1 = fields.Char(string='Cel 1', readonly=False, store=True, tracking=12)
    phone2 = fields.Char(string='Cel 2',  readonly=False, store=True, tracking=12)
    phone3 = fields.Char(string='Cel 3',  readonly=False, store=True, tracking=12)


    email = fields.Char('Email', help="Email of Invited Person")

    razon_social = fields.Char('Website', index=True, store=True, readonly=False)

    website = fields.Char('Website', index=True, help="Website of the contact", store=True, readonly=False)

    country_id = fields.Many2one(string='Pais',required=False, comodel_name='res.country', help="Chen applied on taxes.")

    city_id = fields.Many2one(string='Provincia',required=False, comodel_name='res.city')
    
    district_id = fields.Many2one(string='Distrito', comodel_name='l10n_pe.res.city.district' )

    image =  fields.Binary(string="Imagen")

    
    activo = fields.Boolean('Activo', default=True)




class TodoTask(models.Model):
    _name = 'todo.task'
    name = fields.Char('Nombres', required=False)


class L10nLatamIdentificationType(models.Model):

    _inherit = "l10n_latam.identification.type"

    aaa = fields.Boolean('Activo', default=True)



