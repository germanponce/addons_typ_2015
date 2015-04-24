# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv, orm
from datetime import date, datetime, time, timedelta
from openerp.tools.translate import _


class wizard_consult_invoices(osv.osv_memory): ### Diferencia de un asistente osv_memory
    _name = 'wizard.consult.invoices'
    _description = 'Asistente de Consulta de Facturas'
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Cliente', 
            required=True),
        'start_date': fields.date('Fecha Inicio', required=True),
        'end_date': fields.date('Fecha Final', required=True ),
        'no_pdf': fields.boolean('No Imprimir PDF'),
    }

    def _get_date_start(self, cr, uid, context=None):
        date_now = datetime.now().strftime('%Y-%m-%d')
        date_strp = datetime.strptime(date_now, '%Y-%m-%d')
        year = date_strp.year
        month = date_strp.month
        day = date_strp.day
        print "######### ANO DE LA FECHA ACTUAL >>> ", year
        date_return = date_strp - timedelta(days=30)
        # hours, minutes, seconds, months, years

        return str(date_return)

    def _get_partner(self, cr, uid, context=None):
        print "################### CONTEXT >>> ", context
        if 'active_id' in context:
            active_id = context['active_id']
            print "############### ACTIVE ID >>>> ", active_id
            account_br = self.pool.get('account.invoice').browse(cr,
                uid, active_id, context=None)
            return account_br.partner_id.id
        return False

    _defaults = { 
        'partner_id': _get_partner,
        'end_date': lambda *a: datetime.now().strftime('%Y-%m-%d'),
        'start_date': _get_date_start,
        }

    def process(self, cr, uid, ids, context=None):
        print "################ EJECUTANDO ASISTENTE >>>> "
        account_obj = self.pool.get('account.invoice')
        cr.execute("delete from consult_table_partner;")
        cr.execute("delete from consult_table_partner_lines;")
        for rec in self.browse(cr, uid, ids, context=None):
            account_ids = account_obj.search(cr, uid, [
                ('partner_id','=',rec.partner_id.id),
                ('date_invoice','>=',rec.start_date),
                ('date_invoice','<=',rec.end_date)],
                )
            print "################### ACCOUNT INVOICE IDS >>> ", account_ids
            if account_ids:
                # try:
                # except:
                table_obj = self.pool.get('consult.table.partner')
                amount_total = 0.0
                report_lines = []
                cr.execute(""" 
                select sum(amount_total) from account_invoice
                where id in %s;
                    """, (tuple(account_ids), ) )
                try:
                    amount_total= cr.fetchall()[0][0]
                except:
                    amount_total = 0.0
                #### CONSULTANDO LAS FACTURAS 
                invoice_line = self.pool.get('account.invoice.line')
                #### AGRUPANDO LAS LINEAS DE FACTURA PARA OBTENER LOS PRODUCTOS
                #### SERVICIOS FACTURADOS.
                invoice_line_product_ids = invoice_line.search(cr, uid,
                    [('invoice_id','in',tuple(account_ids)),
                    ('product_id','!=',False)])

                invoice_line_not_product = invoice_line.search(cr, uid,
                    [('invoice_id','in',tuple(account_ids)),
                    ('product_id','=',False)])
                if invoice_line_product_ids: #### Validacion de Facturas con Productos
                    cr.execute(""" 
                    select product_id from account_invoice_line
                    where id in %s group by product_id;
                        """, (tuple(invoice_line_product_ids), ) )

                    result_cr = cr.fetchall()
                    product_ids = [x[0] for x in result_cr] ### Listas Comprehension
                
                    print "###### PRODUCT IDS >>>> ", product_ids

                    for product in product_ids:
                        invoice_list_ids = invoice_line.search(cr, uid,
                            [('product_id','=',product),
                             ('id','in',tuple(invoice_line_product_ids)),
                             ])
                        cr.execute("""
                            select sum(quantity),sum(price_subtotal), name
                            from account_invoice_line where id in %s group by name;
                            """, (tuple(invoice_list_ids), ) )
                        cr_result = cr.fetchall()
                        xline = (0,0,{
                            'product_id': product,
                            'qty': cr_result[0][0],
                            'amount_total': cr_result[0][1],
                            'name': cr_result[0][2],
                            })
                        report_lines.append(xline)
                        print "############### CR RESULT >>>>> ", cr_result
                    amount_global_lines = 0.0
                    amount_negative = 0.0
                    for invoice_line in invoice_line.browse(cr, uid, 
                                        invoice_line_not_product, context=None ):
                        ### EJEMPLOS DE COMPARACIONES Y ACUMULACIONES DE FORMULAS
                        if invoice_line.price_unit < 0.0:
                            amount_negative += invoice_line.price_unit
                        else:
                            manual_subtotal = invoice_line.price_unit * invoice_line.quantity
                            amount_global_lines += manual_subtotal
                        xline = (0,0,{
                            'product_id': invoice_line.product_id.id,
                            'qty': invoice_line.quantity,
                            'amount_total': invoice_line.price_subtotal,
                            'name': invoice_line.name,
                            })
                        report_lines.append(xline)
                print "############## REPORT LINES >>>>> ", report_lines
                vals = {
                    'partner_id': rec.partner_id.id,
                    'start_date': rec.start_date,
                    'end_date': rec.end_date,
                    'amount_total': amount_total,
                    'report_lines': report_lines,
                    }
                report_id = table_obj.create(cr, uid, vals, 
                    context=None) ## Solo retorna un ID
                if rec.no_pdf == True:
                    return {
                        'type': 'ir.actions.act_window',
                        'name': _('Facturas Cliente %s' % rec.partner_id.name),
                        'res_model': 'consult.table.partner',
                        'res_id': report_id,
                        'view_type': 'form',
                        'view_mode': 'form',
                        'view_id': False,
                        'target': 'current', # new
                        'nodestroy': True,
                    }
                #### Retornamos el Reporte ####
                report = {
                'type':'ir.actions.report.xml',
                'report_name':'account.report.webkit.partner',
                'datas' : {
                    'model' : 'consult.table.partner',
                    'ids'   : [report_id],
                    }
                }
                return report
        return True