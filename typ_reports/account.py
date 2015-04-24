# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv, orm

class account_invoice(osv.osv):
    _name = 'account.invoice'
    _inherit ='account.invoice'
    _columns = {
        }

    def print_factura_rml(self, cr, uid, ids, context=None):
        value = {
            'type': 'ir.actions.report.xml',
            'report_name': 'report.account.typ',
            'datas': {
                        'model' : 'account.invoice',
                        'ids'   : ids,
                        }
                    }

        return value