# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv, orm
from datetime import date, datetime, time, timedelta
from openerp.tools.translate import _
import base64

##### LIBRERIAS TRABAJAR CON ARCHIVOS XML ###### 
from xml.dom import minidom
from xml.dom.minidom import Document , parse , parseString
import tempfile

class ir_attachment_facturae_mx(osv.osv):
    _name = 'ir.attachment.facturae.mx' 
    _inherit = 'ir.attachment.facturae.mx'
    _columns = {
    }

    def add_addenta_xml(self, cr, ids, xml_res_str=None, 
                comprobante=None, context=None):
        ### VERIFICAMOS QUE NO TENGA ADDENDA Y SI LA TIENE ENTONCES SIGA EL FLUJO NORMAL SI NO ENTONCES AGREGUE LA INFORMACION
        xml_data = base64.decodestring(base64.encodestring(
            xml_res_str.toxml('UTF-8')))

        have_addenda = 'cfdi:Addenda' in xml_data
        if have_addenda == True:
            return xml_res_str
        xml = super(ir_attachment_facturae_mx, 
            self).add_addenta_xml(cr, ids, xml_res_str, 
            comprobante, context=context)

        return xml
ir_attachment_facturae_mx()


class account_invoice(osv.osv):
    _name = 'account.invoice'
    _inherit ='account.invoice'
    _columns = {
        }

    _defaults = {
        }

    def _get_facturae_invoice_xml_data(self, cr, uid, ids, 
                                                context=None):
        print "################## GENERANDO EL XML >>>> "

        xml_data = super(account_invoice, 
            self)._get_facturae_invoice_xml_data(cr, uid, ids, 
                                                context=context)
        addenda = self.insert_addenda_new(cr, uid, ids, context=None)
        addenda = addenda.replace('<cfdi>','').replace('</cfdi>','')
        original =  ("</cfdi:Comprobante>").encode('utf8')
        replacement = (addenda + "</cfdi:Comprobante>").encode('utf8')
        xml_data_cadena = xml_data[1]
        xml_data_2 =(xml_data[0],xml_data_cadena.replace(original, 
            replacement))
        print "############## XML DATA 2 >>>>> ", xml_data_2
        return xml_data_2
        # return xml_data

    def insert_addenda_new(self, cr, uid, ids, context=None):
        datas_fname = ""
        file_r = ""
        xml_data = ""
        for rec in self.browse(cr, uid, ids, context=None):
            ####################### IMPORTANTE  ########################
            if rec.type in ('out_invoice','out_refund'):
                dom = parseString("<cfdi></cfdi>")
                root = dom.getElementsByTagNameNS('*','cfdi')[0]
                addenda = dom.createElement('cfdi:Addenda') # Creamos nodo Addenda
                root.appendChild(addenda)

                addenda_nueva = dom.createElement('Addenda')
                addenda.appendChild(addenda_nueva)

                etiqueta1 = dom.createElement('EmpresaX')
                addenda_nueva.appendChild(etiqueta1)

                fact = dom.createElement('Factura')
                #### OBTENIENDO EL TC. PARA UN ATRIBUTO DE LA ADDENDA
                cr.execute("""select rate from res_currency_rate
                        where currency_id=%s order by name desc""", 
                    (rec.currency_id.id, ))

                tipo_cambio = cr.fetchall()[0][0]

                fact.setAttribute('Moneda', 
                    rec.currency_id.name)

                fact.setAttribute('TC', str(tipo_cambio))
                fact.setAttribute('NoFactura', rec.number)

                text_f = dom.createTextNode('Detalles de la Factura')
                fact.appendChild(text_f)

                etiqueta1.appendChild(fact)

                data_xml = base64.encodestring(root.toxml('UTF-8'))
                xml_string = base64.decodestring(data_xml)
                print "################## >>>>>> xml string >>>> ", xml_string
                return xml_string

