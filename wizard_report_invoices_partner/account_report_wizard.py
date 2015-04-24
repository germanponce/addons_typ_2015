# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv, orm

class consult_table_partner(osv.osv):
    _name = 'consult.table.partner'
    _description = 'Tabla del Reporte del Asistente'
    _rec_name = 'sequence' ## Permite Enfocar al ORM sobre este C. 
    _columns = {
        # 'name': field.xxx(), Campo Obligatorio
        ### Secuencia
        'sequence': fields.char('Secuencia', size=128),
        'partner_id': fields.many2one('res.partner', 'Cliente'),
        'start_date': fields.date('Fecha Inicio', required=True),
        'end_date': fields.date('Fecha Final', required=True ),
        'amount_total': fields.float('Monto Total Ventas', 
            digits=(15,4) ),

        'report_lines': fields.one2many('consult.table.partner.lines',
            'report_id', 'Productos Vendidos'),
    }

    ######### IMRPIMIR REPORTE DESDE FUNCION ##########
    def print_report(self, cr, uid, ids, context=None):
        report = {
                'type':'ir.actions.report.xml',
                'report_name':'account.report.webkit.partner',
                'datas' : {
                    'model' : 'consult.table.partner',
                    'ids'   : ids,
                    }
                }
        return report

    ##### ASIGNAR SECUENCIA DESDE UN METODO XXXX
    def asign_sequence(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids, context=None):
            if not rec.sequence:
                sequence = self.pool.get('ir.sequence').get(cr, uid, 
                        'consult.table.partner')
                rec.write({'sequence':sequence})
        # self.write(cr, uid, ids, {'sequence':sequence}, context=None)

        return True

    # CREATE => CREA UN REGISTRO
    # UNLINK => ELIMINA UN REGISTRO
    # WRITE => ACTUALIZA UN REGISTRO
    ##### ASIGNAR SECUENCIA DESDE QUE SE CREA EL REGISTRO 
    def create(self, cr, uid, vals, context=None):
        ### CONSULTANDO LA SECUENCIA
        sequence = self.pool.get('ir.sequence').get(cr, uid, 
                        'consult.table.partner')
        if sequence:
            vals['sequence'] = sequence

        return super(consult_table_partner, self).create(cr, uid, 
            vals, context=context)

    _order = 'sequence' 

class consult_table_partner_lines(osv.osv):
    _name = 'consult.table.partner.lines'
    _description = 'Lineas delReporte'
    # _rec_name = 'product_id' 
    _columns = {
        'report_id': fields.many2one('consult.table.partner',
         'ID Ref.'),
        'product_id': fields.many2one('product.product', 'Producto'),
        'qty': fields.float('Cantidad', digits=(14,2)),
        'amount_total': fields.float('Total Vendido', digits=(14,2) ),
        'name': fields.char('Descripcion', size=128),
    }

    _order = 'name' 
