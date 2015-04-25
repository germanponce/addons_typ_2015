# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv, orm
from tools.translate import _
from openerp import tools

class analisis_stock_in(osv.osv):
    _name = 'analisis.stock.in'
    _auto = False ### NO CREE LA TABLA DE FORMA AUTOMATICA
    _description = 'Analisis de Entradas de Almacen'
    _columns = {
        'id': fields.integer('ID Analisis'),
        'name': fields.char('Albaran'),
        'total_entrada': fields.float('Total Entradas',
            digits=(14,2)),
        'date': fields.datetime('Fecha'),
        'supplier_id': fields.many2one('res.partner','Proveedor'),

    }
    ###### EL ANALISIS EJECUTA ESTA FUNCION DESDE SU INSTALACION
    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'analisis_stock_in')
        cr.execute("""
            create or replace view analisis_stock_in as (
                SELECT sp.id as id,
                        sp.partner_id as supplier_id,
                        sp.name,
                        sum(product_qty) as total_entrada,
                        sp.date
                        
                    FROM stock_picking sp 
                        LEFT JOIN stock_move sm
                            ON (sm.picking_id = sp.id)
                        
                    WHERE 
                          sp.type = 'in'
                    GROUP BY sp.id
                
            )""")