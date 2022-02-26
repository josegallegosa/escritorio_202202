# -*- coding: utf-8 -*-
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class HrAccountJournalInherit(models.Model):
    _inherit = 'account.journal'

    journal_ids = fields.One2many(comodel_name='account.fiscal.position.account.template.secondary',inverse_name='journal_id')


    def map_account(self, account):
        for pos in self.journal_ids:
            if pos.account_src_id.id == account:
                return pos.account_dest_id.id
        return account