# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv, orm
from datetime import date, datetime, time, timedelta
from openerp.tools.translate import _
import base64
####### TRABAJAR CON LOS EXCEL
import xlsxwriter
import tempfile
##### SOLUCIONA CUALQUIER ERROR DE ENCODING (CARACTERES ESPECIALES)
import sys
reload(sys)  
sys.setdefaultencoding('utf8')


class consult_export_csv_excel (osv.osv_memory):
    _name = 'consult.export.csv.excel'
    _description = 'Exportar Consulta a Excel o CSV'
    _columns = {
        'datas_fname': fields.char('File Name',size=256),
        'file': fields.binary('Layout'),
        'download_file': fields.boolean('Descargar Archivo'),
        'cadena_decoding': fields.text('Binario sin encoding'),
        'type': fields.selection([('csv','CSV'),
                                ('xls','Excel')], 'Tipo Exportacion', 
                                required=True, ),
    }

    _defaults = {
        'download_file': False,
        'type': 'csv',
        }

    def export_xls_file(self, cr, uid, ids, context=None):
        document_csv = ""
        active_ids = context['active_ids']
        consult_obj = self.pool.get('consult.table.partner')
        if active_ids:
            for rec in self.browse(cr, uid, ids, context=None):
                consult_br = consult_obj.browse(cr, uid, active_ids,
                                                  context=None)[0]
                ####### CREANDO UN NUEVO EXCEL WORKBOOK
                fname = tempfile.NamedTemporaryFile(suffix='.xlsx',
                                                        delete=False)
                print "#################### >>>>> TEM NAME >>>>>",fname
                workbook = xlsxwriter.Workbook(fname)
                worksheet = workbook.add_worksheet()
                ####### SELECCIONANDO EL RANGO DE CELDAS PARA TRABAJAR
                worksheet.set_column('A:K', 20)
                ##### ESTILOS CELDAS 
                bold = workbook.add_format({'bold': True})

                format_red = workbook.add_format({'bold': True})

                format_red.set_bg_color('#2E72D9')
                format_red.set_align('center')
                format_red.set_font_color('white')

                format_center = workbook.add_format()
                format_center.set_align('center')

                # Cabeceras
                worksheet.write('A1', 'Cliente', format_red)
                worksheet.write('B1', 'Fecha Inicio', format_red)
                worksheet.write('C1', 'Fecha Fin', format_red)
                worksheet.write('D1', 'Monto Total', format_red)

                worksheet.write('A2', consult_br.partner_id.id, format_center)
                worksheet.write('B2', consult_br.start_date, format_center)
                worksheet.write('C2', consult_br.end_date, format_center)
                worksheet.write('D2', consult_br.amount_total, format_center)

                #### DETALLE DE LAS LINEAS
                worksheet.write('A4', 'Detalle de Facturas', format_red)

                worksheet.write('A5', 'Descripcion', format_red)
                worksheet.write('B5', 'Producto', format_red)
                worksheet.write('C5', 'Cantidad', format_red)
                worksheet.write('D5', 'Subtotal', format_red)

                i = 6
                for linea in consult_br.report_lines:

                    worksheet.write('A'+str(i), linea.name, bold)
                    worksheet.write('B'+str(i), linea.product_id.name if 
                                            linea.product_id else '', bold)
                    worksheet.write('C'+str(i), linea.qty, bold)
                    worksheet.write('D'+str(i), linea.amount_total, bold)
                    i += 1
                ##### Finalizando la Escritura del Excel
                workbook.close()
                #### LO LEEMOS PARA ENCODEARLO A LA BASE ####
                f = open(fname.name, "r")
                data = f.read()
                f.close()
                datas_fname = "Consulta "+consult_br.partner_id.name+".xlsx" # Nombre del Archivo
                ##### ESCRIBIR EL RESULTADO EN LA BASE DE DATOS
                rec.write({'cadena_decoding':document_csv,
                    'datas_fname':datas_fname,
                    'file':base64.encodestring(data),
                    'download_file': True})
        return  {
            'type': 'ir.actions.act_window',
            'res_model': 'consult.export.csv.excel',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': ids[0],
            'views': [(False, 'form')],
            'target': 'new',
            }


    def export_csv_file(self, cr, uid, ids, context=None):
        document_csv = ""
        print "############## CONTEXT ==> ", context
        active_ids = context['active_ids']
        consult_obj = self.pool.get('consult.table.partner')
        if active_ids:
            for rec in self.browse(cr, uid, ids, context=None):
                consult_br = consult_obj.browse(cr, uid, active_ids,
                                                    context=None)[0]
                salto_line = "\n"
                cabeceras_p = "Cliente"+","+"Fecha Inicio"\
                            +","+"Fecha Final"+","+"Monto Total Venta"
                document_csv = document_csv + cabeceras_p

                linea_1 = consult_br.partner_id.name+","+\
                consult_br.start_date+","+consult_br.end_date+","+\
                str(consult_br.amount_total)

                document_csv = document_csv + salto_line + linea_1 + salto_line

                cabeceras_l = "Descripcion"+","+"Producto"+","+\
                "Cantidad"+","+"Total"

                texto_x = "Lineas de Facturas"+","+","+","
                document_csv = document_csv+ salto_line+texto_x

                document_csv = document_csv+ salto_line+cabeceras_l

                detalle_lineas = ""
                for linea in consult_br.report_lines:
                    linea_str = ""
                    if linea.product_id:
                        linea_str = str(linea.name)+","+" "+\
                        ","+str(linea.qty)+","+str(linea.amount_total)
                    else:
                        linea_str = str(linea.name)+","+str(linea.product_id.name)+\
                        ","+str(linea.qty)+","+str(linea.amount_total)

                    detalle_lineas = detalle_lineas+salto_line+linea_str
                document_csv = document_csv+detalle_lineas
                datas_fname = "Consulta "+consult_br.partner_id.name+".csv" # Nombre del Archivo
                rec.write({'cadena_decoding':document_csv,
                    'datas_fname':datas_fname,
                    'file':base64.encodestring(document_csv),
                    'download_file': True})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'consult.export.csv.excel',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': ids[0],
            'views': [(False, 'form')],
            'target': 'new',
            }

    def process_export(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids, context=context):
            if rec.type == 'csv':
                result = self.export_csv_file(cr, uid, ids, context=context)
                return result
            else:
                result = self.export_xls_file(cr, uid, ids, context=context)
                return result
        return True