# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv, orm
from datetime import date, datetime, time, timedelta
from openerp.tools.translate import _
import base64

##### LIBRERIAS TRABAJAR CON ARCHIVOS XML ###### 
from xml.dom import minidom
from xml.dom.minidom import Document , parse , parseString
import tempfile

class cfdi_addendas_manager (osv.osv_memory):
    _name = 'cfdi.addendas.manager'
    _description = 'Generacion de una Addenda'
    _columns = {
        'datas_fname': fields.char('File Name',size=256),
        'file': fields.binary('Layout'),
        'download_file': fields.boolean('Descargar Archivo'),
        'cadena_decoding': fields.text('Binario sin encoding'),
        'invoice_id': fields.many2one('account.invoice',
                                        'Factura Timbrada', 
                                        required=True, ),
    }


    def _get_active_id(self, cr, uid, context=None):
        active_id = context['active_id']
        if active_id:
            return active_id
        return False

    _defaults = {
        'download_file': False,
        'invoice_id': _get_active_id,
        }

    def process_addenda(self, cr, uid, ids, context=None):

        datas_fname = ""
        file_r = ""
        xml_data = ""
        for rec in self.browse(cr, uid, ids, context=context):
            print "############## FACTURA >>> ", rec.invoice_id.number
            if rec.invoice_id.type in ("out_invoice","out_refund"):
                account_browse = rec.invoice_id #### Browse Record de la Factura Seleccionada
                attachment_xml_ids = self.pool.get('ir.attachment').search(cr, 
                    uid, [('res_model','=','account.invoice'),
                    ('res_id','=',account_browse.id),
                    ('name','like','.xml')], context=context)
                print "############### ATTACHMENT IDS >>>>> ", attachment_xml_ids
                if attachment_xml_ids:
                    attach_br = self.pool.get('ir.attachment').browse(cr, uid,
                                                attachment_xml_ids, context=context)[0]
                    datas_fname = attach_br.name
                    xml_data = attach_br.index_content
                    print "######## XML >>>>>> ", xml_data
                    dom = parseString(xml_data)
                    root = dom.getElementsByTagNameNS('*', 'Comprobante')[0]
                    addenda = dom.getElementsByTagName('cfdi:Addenda')[0]

                    addenda_nueva = dom.createElement('Addenda')
                    addenda.appendChild(addenda_nueva)

                    etiqueta1 = dom.createElement('EmpresaX')
                    addenda_nueva.appendChild(etiqueta1)

                    fact = dom.createElement('Factura')
                    #### OBTENIENDO EL TC. PARA UN ATRIBUTO DE LA ADDENDA
                    cr.execute("""select rate from res_currency_rate
                            where currency_id=%s order by name desc""", 
                        (account_browse.currency_id.id, ))

                    tipo_cambio = cr.fetchall()[0][0]

                    fact.setAttribute('Moneda', 
                        account_browse.currency_id.name)

                    fact.setAttribute('TC', str(tipo_cambio))
                    fact.setAttribute('NoFactura', account_browse.number)

                    text_f = dom.createTextNode('Detalles de la Factura')
                    fact.appendChild(text_f)

                    etiqueta1.appendChild(fact)


                    ### EL  root.getElementsByTagNames('*','Comprbante') Extrae la cadena y la convierte a UTF8
                    rec.write({'datas_fname':datas_fname,
                        'file':base64.encodestring(root.toxml('UTF-8')),
                        'download_file': True})



        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cfdi.addendas.manager',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': ids[0],
            'views': [(False, 'form')],
            'target': 'new',
            }