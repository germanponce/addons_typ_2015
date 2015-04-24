# -*- encoding: utf-8 -*-

from report import report_sxw
from report_webkit import report_helper
from report_webkit import webkit_report
from openerp.osv import fields, osv, orm
import time

class account_report_typ(report_sxw.rml_parse): 
    def __init__(self, cr, uid, name,context=None): 
        super(account_report_typ, self).__init__(cr, uid, 
            name, context=context) 
        
        self.localcontext.update({ 
            'time': time,
        })


report_sxw.report_sxw( 
    'report.account.report.typ', 
    'account.invoice', 
    'typ_reports/report/account.rml',
    parser=account_report_typ,
    header=False 
    )
 
 ############ MAKO #############
class account_report_webkit(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_report_webkit, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })

report_sxw.report_sxw('report.account.report.webkit',
                    'account.invoice',
                    'typ_reports/report/account.mako',
                    parser=account_report_webkit)
