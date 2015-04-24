# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv, orm

###### HERENCIA A LINEAS DEL PEDIDO #######
class sale_order_line(osv.osv):
    _name = 'sale.order.line'
    _inherit ='sale.order.line'
    _columns = {
        'special_sale': fields.boolean('Venta Especial'),
        'ref_customer': fields.char('Referencia Cliente', size=128),
        }
###### HERENCIA DE PEDIDO DE VENTA #######
class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit ='sale.order'
    _columns = {
        }
    ######## HERENCIA AL METODO CONFIRMAR PEDIDO DE VENTA ######
    def action_button_confirm(self, cr, uid, ids, context=None):
        res = super(sale_order, self).action_button_confirm(cr, uid, ids,
         context)
        print "############## CONFIRMANDO PEDIDO DE VENTA >>>> "
        print "############## CONFIRMANDO PEDIDO DE VENTA >>>> "
        purchase_obj = self.pool.get('purchase.order')
        self_br = self.browse(cr, uid, ids, context=None)[0]
        print "##################### SELF BR >>>> ", self_br
        print "##################### SELF BR >>>> ", self_br.name
        print "##################### SELF BR >>>> ", self_br.pricelist_id.name

        purchase_ids = purchase_obj.search(cr, uid, 
            [('origin','=',self_br.name)])
        # cr.execute("""select id from purchase_order 
        #     where origin ='%s' """ % (self_br.name,))
        # sql_cr = cr.fetchall()
        # print "############# RESULTADO DE QUERY SQL >>>> ",sql_cr
        print "#################### PURCHASE IDS >>>>>> ", purchase_ids
        ###### BUSCANDO PEDIDOS DE COMPRA LIGADOS A VENTA #####
        purchase_line_obj = self.pool.get('purchase.order.line')
        if purchase_ids:
            for line in self_br.order_line:
                if line.type == 'make_to_order':
                    purchase_line_ids = purchase_line_obj.search(cr, uid,
                        [('product_id','=',line.product_id.id),
                        ('order_id','in',tuple(purchase_ids))])
                    if purchase_line_ids:
                        purchase_line_obj.write(cr, uid, purchase_line_ids,
                             {
                             'special_sale': line.special_sale,
                              'ref_customer': line.ref_customer,
                              })
                    ### EQUIVALENTE A CODIGO SQL ###
                    # cr.execute("""update purchase_order_line set 
                    #     special_sale=%s,
                    #     ref_customer=%s where id in %s;
                    #     """, (line.special_sale, line.ref_customer, 
                    #         tuple(purchase_line_ids)))

        return res

###### HERENCIA A LINEAS DEL COMPRA #######
class purchase_order_line(osv.osv):
    _name = 'purchase.order.line'
    _inherit ='purchase.order.line'
    _columns = {
        'special_sale': fields.boolean('Venta Especial'),
        'ref_customer': fields.char('Referencia Cliente', size=128),
        }