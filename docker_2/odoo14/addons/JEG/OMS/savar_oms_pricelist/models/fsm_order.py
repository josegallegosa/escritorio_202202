from odoo import api, fields, models


class FsmOrder(models.Model):
    _inherit = 'fsm.order'

    code_merchant = fields.Char(string='Orden comerciante')
    service_id = fields.Many2one('fsm.order.service', string='Servicio')
    subservice_id = fields.Many2one('fsm.order.service', string='Subservicio')


    by_package_id = fields.Many2one('by.package', string='Tipo de bulto')
    payment_type_id = fields.Many2one('payment.type', string='Medio de Pago')
    shipping_type = fields.Char(string='Tipo de envío')
    consigned_id = fields.Char(string='Datos del consignado')

    date_dispatch = fields.Date(string='Fecha de despacho')
    appointment_time_from = fields.Selection(
    	string="hora cita desde",
    	selection=[
    		('8_00_am', '08:00 AM'),
    		('8_30_am', '08:30 AM'),
    		('9_00_am', '09:00 AM'),
    		('9_30_am', '09:30 AM'),
    		('10_00_am', '10:00 AM'),
    		('10_30_am', '10:30 AM'),
    		('11_00_am', '11:00 AM'),
    		('11_30_am', '11:30 AM'),
    		('12_00_am', '12:00 AM'),
    		('12_30_am', '12:30 AM'),
    		('01_00_am', '01:00 AM'),
    		('01_30_am', '01:30 AM'),
    		('02_00_am', '02:00 AM'),
    		('02_30_am', '02:30 AM'),
    		('03_00_am', '03:00 AM'),
    		('03_30_am', '03:30 AM'),
    		('04_00_am', '04:00 AM'),
    		('04_30_am', '04:30 AM'),
    		('05_00_am', '05:00 AM'),
    		('05_30_am', '05:30 AM'),
    		('06_00_am', '06:00 AM'),
    		('06_30_am', '06:30 AM'),
    		
    	], default="8_00_am"
    )

    appointment_time_until = fields.Selection(
    	string="hora cita hasta",
    	selection=[
    		('8_00_am', '08:00 AM'),
    		('8_30_am', '08:30 AM'),
    		('9_00_am', '09:00 AM'),
    		('9_30_am', '09:30 AM'),
    		('10_00_am', '10:00 AM'),
    		('10_30_am', '10:30 AM'),
    		('11_00_am', '11:00 AM'),
    		('11_30_am', '11:30 AM'),
    		('12_00_am', '12:00 AM'),
    		('12_30_am', '12:30 AM'),
    		('01_00_am', '01:00 AM'),
    		('01_30_am', '01:30 AM'),
    		('02_00_am', '02:00 AM'),
    		('02_30_am', '02:30 AM'),
    		('03_00_am', '03:00 AM'),
    		('03_30_am', '03:30 AM'),
    		('04_00_am', '04:00 AM'),
    		('04_30_am', '04:30 AM'),
    		('05_00_am', '05:00 AM'),
    		('05_30_am', '05:30 AM'),
    		('06_00_am', '06:00 AM'),
    		('06_30_am', '06:30 AM'),
    		
    	], default="8_30_am"
    )

