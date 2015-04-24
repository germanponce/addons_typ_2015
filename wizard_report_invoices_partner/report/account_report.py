# -*- encoding: utf-8 -*-

from report import report_sxw
from report_webkit import report_helper
from report_webkit import webkit_report
from openerp.osv import fields, osv, orm
import time

 ############ MAKO #############
class account_consult_partner(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_consult_partner, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })

report_sxw.report_sxw('report.account.partner.webkit',
                    'consult.table.partner',
                    'wizard_report_invoices_partner/report/account.mako',
                    parser=account_consult_partner)
