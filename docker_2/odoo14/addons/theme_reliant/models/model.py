# -*- coding: utf-8 -*-
import logging

import uuid

from odoo import fields, models, api

_logger = logging.getLogger(__name__)



class ThemeBeauty(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_reliant_post_copy(self, mod):
        self.disable_view('website.template_header_default')
        self.enable_view('theme_reliant.template_header_magazine_proyect_reliant')
        self.disable_view('website.footer_custom')
        self.enable_view('theme_reliant.footer_reliant')


class reliant_project(models.Model):
    _name = 'reliant.project'
    _description = 'Project Reliant'
    _rec_name = 'name'

    name = fields.Char(string='Project')
    location_country = fields.Many2one(string='Country',required=False, comodel_name='res.country')
    location_city = fields.Many2one('res.city', string='City')
    client_id  = fields.Many2one(comodel_name='reliant.client', string='Client')
    commodity = fields.Char(string='Commodity')
    description = fields.Html(string='Description')
    image =  fields.Binary(string="Image")
    image_detail_1 = fields.Binary(string="Image Detail 1")
    image_detail_2 = fields.Binary(string="Image Detail 2")
    image_detail_3 = fields.Binary(string="Image Detail 3")
    services_ids = fields.Many2many('reliant.service',
        'reliant_project_reliant_service_rel',
        string='Services')

    #fieldmany2many = fields.Many2Many('model.name','your_many2many_table_name','colum1','colum2',string="my many2many field")




class reliant_service(models.Model):
    _name = 'reliant.service'
    _description = 'Service Reliant'
    _rec_name = 'name_service'

    name_service = fields.Char(string='Service')
    description_service = fields.Html(string='Description')
    sequence = fields.Integer(string="Sequence")
    projects_ids = fields.Many2many('reliant.project',
        'reliant_project_reliant_service_rel',
        string='Projects')


class reliant_job_department(models.Model):
    _name = 'reliant.job.department'
    _description = 'Reliant Job Opportunity Department'

    name = fields.Char(string='Department')

class reliant_job_site(models.Model):
    _name = 'reliant.job.site'
    _description = 'Reliant Job Opportunity Site'

    name = fields.Char(string='Site')

class reliant_job_language(models.Model):
    _name = 'reliant.job.language'
    _description = 'Language Job Opportunity Reliant'

    name = fields.Char(string='Language')

class reliant_job_position(models.Model):
    _name = 'reliant.job.position'
    _description = 'Reliant Job Opportunity Position'


    name = fields.Char(string='Position')
class reliant_job_location(models.Model):
    _name = 'reliant.job.location'
    _description = 'Location Opportunity Job Reliant'

    name = fields.Char(string='Location')

class reliant_job_category(models.Model):
    _name = 'reliant.job.category'
    _description = 'Category Closure Reliant Job Opportunity'

    name = fields.Char(string='Category')

class reliant_client(models.Model):
    _name = 'reliant.client'
    _description = 'Client Reliant'
    
    name = fields.Char(string='Client')
    image_1920 = fields.Binary(string="Company logo")
    to_show_home = fields.Boolean(string="To show home", default=True)


class reliant_job_opportunity(models.Model):
    _name = 'reliant.job.opportunity'
    _description = 'Reliant Job Opportunity'
    _rec_name = 'client_id'

    country = fields.Many2one(comodel_name='res.country', string='Country')
    department = fields.Many2one('reliant.job.department', string='Department')
    site = fields.Many2one('reliant.job.site', string='Site')
    language = fields.Many2one('reliant.job.language', string='Language')
    position = fields.Many2one('reliant.job.position', string='Position')
    location = fields.Many2one('reliant.job.location', string='Location')
    closing_date = fields.Date(string='Closing date')
    description_job_opportunity = fields.Html(string='Description')
    category_job_opportunity = fields.Many2one('reliant.job.category', string='Category')
    state = fields.Selection(
        string="State",
        selection=[
            ('cancel', 'Cancelled'),
            ('confirm', 'Confirmed'),
            ('draft', 'Draft'),
        ], default="confirm"
    )  
    img_job = fields.Binary(string="Image Employment")
    client_id  = fields.Many2one(comodel_name='reliant.client', string='Client')
    
class reliant_policy_standard_principle(models.Model):
    _name = 'reliant.policy.standard.principle'
    _description = 'Policies, standards and principles'
    
    name = fields.Char(string='Policies, standards and principles')

class reliant_pdf_value(models.Model):
    _name = 'reliant.pdf.value'
    _description = 'Archive PDF Reliant'
    _rec_name = 'attachment_id'

    attachment_id = fields.Many2one('ir.attachment',string='Archive PDF',required="true")
    policy_standard_principle = fields.Many2one ('reliant.policy.standard.principle',string='Policies, standards and principles')


    def write(self, vals):
        if vals.get('attachment_id') :
            self.env['ir.attachment'].search([('id', '=', self.attachment_id.id)]).generate_access_token() 
        return super(reliant_pdf_value, self).write(vals)
    

    @api.model
    def create(self, vals):
        print("create",vals)
        if vals.get('attachment_id') :
            self.env['ir.attachment'].search([('id', '=', vals.get('attachment_id'))]).generate_access_token() 

        return super(reliant_pdf_value, self).create(vals)    

    
    