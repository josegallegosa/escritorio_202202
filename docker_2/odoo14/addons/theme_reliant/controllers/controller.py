# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request,content_disposition
from odoo.addons.website_sale.controllers.main import WebsiteSale
import json
import logging
import base64
import werkzeug

class WebsiteBinary(http.Controller):
    @http.route('/projects', type='http', auth="public", website=True, sitemap=True)
    def proyectos(self, **kw):
        projects = request.env['reliant.project'].sudo().search([])
        list_proj_countries = []
                
        for proj in projects:
            if proj.location_country.id not in list_proj_countries:
                list_proj_countries.append(proj.location_country.id)

        values={
            'projects':projects,
            'countries': request.env['res.country'].sudo().search([('id','in',list_proj_countries)]),
        }
        
        return request.render("theme_reliant.projects", values)
        
    @http.route('/services', type='http', auth="public", website=True, sitemap=True)
    def servicios(self, **kw):
        services = request.env['reliant.service'].sudo().search([],order='sequence')
        values_service = services.mapped(lambda x: [x.id,x.name_service, x.description_service])
        projects_initial = request.env['reliant.project'].sudo().search([],limit=3)
        values_project_initial = projects_initial.mapped(lambda x: [x.id,x.name, x.image])

        for x in values_service:
            x[2]=x[2].replace("<p>","").replace("</p>","").replace("<b>","").replace("</b>","").replace("<br>","").replace("</br>","")



        values={
            'services':values_service,
            'values_project_initial':values_project_initial,
        }    
        return request.render("theme_reliant.services", values)

    @http.route(['/jsonservices'], type='json', methods=['POST'], auth="public", website=True)
    def jsonServices(self, service):
        service_id = request.env['reliant.service'].sudo().browse(int(service))
        values_service = service_id.mapped(lambda x: [x.id,x.name_service, x.description_service])


        values={
             'values_service':values_service,
        }
        
        return values

    @http.route(['/ajaxtocontroller_service'], type='json', methods=['POST'], auth="public", website=True)
    def changeServicios(self, service):
        list_serv = []
        list_serv.append(service)
        allprojects = request.env['reliant.project'].sudo().search([('services_ids','in',list_serv)],limit=3)
        values_project = allprojects.mapped(lambda x: [x.id,x.name, x.image])

        values={
            'project':values_project,
        }
        
        return values

    @http.route(['/openmodalproject'], type='http', methods=['POST'], auth="public", csrf=False)
    def changeProjectsModal(self, **post):
        project = post['project']
        project_id = request.env['reliant.project'].sudo().browse(int(project))
        
        l_modal_project = []

        list_serv = []


        for x in project_id :
            for s in  x.services_ids :
                if s.name_service not in list_serv:
                    list_serv.append(s.name_service)
            l_modal_project.append({
                'id': x.id,
                'project_name': x.name,  
                'image_detail_1': x.image_detail_1.decode(), 
                'image_detail_2': x.image_detail_2.decode(), 
                'image_detail_3': x.image_detail_3.decode(), 
                'client_id_name': x.client_id.name,
                'client_id_image': x.client_id.image_1920.decode(),
                'location_country': x.location_country.name,
                'location_city': x.location_city.name,
                'commodity': x.commodity,
                'servicios':list_serv
                })


    

        values={
             'project_modal':l_modal_project,
        }
        
        return json.dumps(values)


    @http.route(['/openmodaljob'], type='http', methods=['POST'], auth="public", csrf=False)
    def changeJobsModal(self, **post):
        job = post['job']

        job_id = request.env['reliant.job.opportunity'].sudo().browse(int(job))

        l_modal_job = []

        for x in job_id :
            l_modal_job.append({
                'id': x.id,
                'position': x.position.name, 
                'location': x.location.name, 
                'description_job_opportunity': x.description_job_opportunity, 
                'img_job': x.img_job.decode(), 
                'client_id': x.client_id.name, 
                'client_id_image_1920': x.client_id.image_1920.decode() 
                })
   
        values={
             'job_modal': l_modal_job
        }
        return json.dumps(values) 

    @http.route(['/filterpdf'], type='http', methods=['POST'], auth="public", csrf=False)
    def changePdfValue(self, **post):
        pdf = post['pdf']
        pdf_id = request.env['reliant.policy.standard.principle'].sudo().browse(int(pdf))
        
        l_modal_pdf = []

        for x in pdf_id :
            l_modal_pdf.append({
                'id': x.id,
                'name_value': x.name,  
                })

        values={
             'pdf_filter':l_modal_pdf,
        }
        print(values)
        return json.dumps(values)

    @http.route(['/services/<model("reliant.service"):service_id>'], type='http', auth="public", website=True, sitemap=False)
    def servicios_detalle(self, service_id, **post):
        values={
            'service':service_id
        }
        return request.render("theme_reliant.services_details", values)

    @http.route('/home', type='http', auth="public", website=True, sitemap=True)
    def home(self, **kw):
        home_to_projects = request.env['reliant.project'].sudo().search([],limit=3)
        project_home = home_to_projects.mapped(lambda y: (y.id, y.name, y.image ))

        customers = request.env['reliant.client'].sudo().search([])
        customers_type = customers.mapped(lambda x: (x.id,x.image_1920,x.to_show_home))
 

        return request.render("theme_reliant.home",{'customers_type':customers_type, 'project_home':project_home})

    @http.route('/about', type='http', auth="public", website=True, sitemap=True)
    def about(self, **kw):
        return request.render("theme_reliant.about")



    @http.route('/sustainability', type='http', auth="public", website=True, sitemap=True)
    def sustainability(self, **kw):
        pdf_values = request.env['reliant.pdf.value'].sudo().search([])
        pdf_values_type = request.env['reliant.policy.standard.principle'].sudo().search([])
        
        values = pdf_values.mapped(lambda x: [x.attachment_id.id, x.attachment_id.name, x.policy_standard_principle.id])
        for value in  values :
            document = request.env['ir.attachment']
            document = document.sudo().search([('id', '=', value[0])])
            base_url = request.env['ir.config_parameter'].sudo().search([('key', '=', 'web.base.url')]).value
            url = base_url + "/web/content/"+str(value[0])+"?download=true&access_token="+document.access_token
            value[0]=url
        values_type = pdf_values_type.mapped(lambda x: (x.id,x.name))
        """
        document = request.env['ir.attachment']
        document = document.sudo().search([('id', '=', pdf_id)])
        base_url = request.env['ir.config_parameter'].sudo().search([('key', '=', 'web.base.url')]).value
        
        
        url = base_url + "/web/content/"+pdf_id+"?download=true&access_token="+document.access_token
           """   
        return request.render("theme_reliant.sustainability",{'values':values,'values_type':values_type})
        




    
    @http.route('/contacts', type='http', auth="public", website=True, sitemap=True)
    def contacts(self, **kw):
        return request.render("theme_reliant.contacts")

    @http.route(['/job_opportunities/<model("reliant.job.opportunity"):job_id>'], type='http', auth="public", website=True, sitemap=False)
    def job_detail(self, job_id, **post):
        values={
            'job':job_id
        }
        return request.render("theme_reliant.job_opportunities_detail", values)


    @http.route('/job_opportunities', type='http', auth="public", website=True, sitemap=True)
    def jobs_opportunities(self, **kw):
        opportunities = request.env['reliant.job.opportunity'].sudo().search([])

        l_country = []
        l_department = []
        l_site = []
        l_language = []
        for o in opportunities:
            if o.country.id not in l_country:
                l_country.append(o.country.id)
            if o.department.id not in l_department:
                l_department.append(o.department.id)
            if o.site.id not in l_site:
                l_site.append(o.site.id)
            if o.language.id not in l_language:
                l_language.append(o.language.id)

        


        values={
            'opportunities':opportunities,
            'countries':request.env['res.country'].sudo().search([('id','in',l_country)]),
            'departments':request.env['reliant.job.department'].sudo().search([('id','in',l_department)]),
            'sites':request.env['reliant.job.site'].sudo().search([('id','in',l_site)]),
            'languages_opportunity':request.env['reliant.job.language'].sudo().search([('id','in',l_language)]),
        }    
        return request.render("theme_reliant.job_opportunities", values)


    @http.route(['/change/job'], type='json', methods=['POST'], auth="public", website=True)
    def changeJob(self, country, department, site, language):
        print(country, department, site, language)

        dominio = []

        if int(country) != 0: 
            dominio.append(('country','=',int(country)))
        if int(department) != 0: 
            dominio.append(('department','=',int(department)))
        if int(site) != 0: 
            dominio.append(('site','=',int(site)))
        if int(language) != 0: 
            dominio.append(('language','=',int(language)))

        op = []

        opportunities = request.env['reliant.job.opportunity'].sudo().search(dominio)

        for o in opportunities:
            op.append({
                'id':o.id,
                'position': o.position.name,
                'location': o.location.name,
                'site': o.site.name,
                'closing_date': o.closing_date,
                'category_job_opportunity': o.category_job_opportunity.name,
                'description_job_opportunity': o.description_job_opportunity,
                })
                

        return {'opportunities':op}


    @http.route(['''/contacts/thank-you'''], type='http', auth="public", website=True)
    def send_email_contactus(self, **post):
        txt = ''
        if post['type_here']:
            txt += 'Type Here: '+post['type_here']+' <br>'
        
        #FIX IT , APPEND TEMPLATE
        valuesmail = {
            'subject':'RELIANT - '+post['your_name']+' '+post['last_name'], 
            'body_html':txt, 
            'email_from':post['email'], 
            'email_to':post['email_company'], 
            }
        mail = request.env['mail.mail'].sudo().create(valuesmail)
        
        try:
            mail.send()
        except:
            return request.render("theme_reliant.contacts")

        return request.render("theme_reliant.contacts-thanks")