from odoo import http, _
from odoo.http import request
from odoo.exceptions import Warning, UserError
from odoo.addons.portal.controllers.portal import CustomerPortal
import logging, sys
_logger = logging.getLogger(__name__)

class CustomerPortalInerith(CustomerPortal):
    OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name", "merchant_catalog_owner"]

    