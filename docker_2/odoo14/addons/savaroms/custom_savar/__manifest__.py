# -*- coding: utf-8 -*-
{
    'name': "custom_savar",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_management', 'account', 'crm', 'website', 'stock', 'purchase', 'website_sale', 'hr_expense', 'fleet', 'im_livechat', 'board', 'hr_attendance', 'agreement_legal', 'auditlog', 'base_territory', 'fieldservice', 'helpdesk_mgmt', 'pim', 'product_configurator', 'purchase_request', 'shopfloor', 'shopfloor_base', 'shopfloor_batch_automatic_creation', 'shopfloor_delivery_shipment', 'shopfloor_packing_info', 'website_product_configurator', 'hw_escpos', 'base_automation', 'contract_sale', 'partner_company_group', 'product_margin', 'sale_margin', 'sale_order_ubl', 'sale_product_matrix', 'sale_shipping_info_helper', 'sales_team_security', 'l10n_pe', 'delivery', 'procurement_jit', 'product_expiry', 'purchase_order_line_menu', 'purchase_product_matrix', 'purchase_requisition', 'shopfloor_delivery_shipment_mobile', 'shopfloor_mobile_base_auth_user', 'shopfloor_workstation', 'shopfloor_workstation_mobile', 'stock_dropshipping', 'stock_picking_batch', 'stock_putaway_method', 'website_crm', 'website_animate', 'website_form', 'website_sale_order_type', 'website_sale_product_attribute_filter_category', 'website_sale_product_attribute_filter_category', 'website_sale_product_description', 'website_sale_product_detail_attribute_image', 'website_sale_stock', 'website_sale_stock_available', 'fleet_vehicle_category', 'fleet_vehicle_history_date_end', 'fleet_vehicle_inspection', 'fleet_vehicle_inspection_template', 'fleet_vehicle_service_calendar', 'fleet_vehicle_service_kanban', 'hr_employee_firstname', 'hr_expense_invoice', 'barcodes', 'google_account', 'google_recaptcha', 'product_supplierinfo_barcode', 'test_access_rights', 'test_performance', 'test_xlsx_export', 'web_tree_dynamic_colored_field', 'web_tree_many2one_clickable', 'web_widget_bokeh_chart', 'web_widget_char_size', 'web_widget_x2many_2d_matrix', 'test_mail_full', 'odoope_ruc_validation', 'base_partner_sequence', 'sql_export_excel', 'base_location_geonames_import'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
