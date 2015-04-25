# -*- encoding: utf-8 -*-

{
    'name': 'Tablero de Prueba / Creacion de Analisis',
    'version': '1',
    "author" : "Argil C.",
    "category" : "TyP",
    'description': """

        Tablero de Prueba con Datos de Venta
        Ejemplo de Analisis

    """,
    "website" : "http://www.argil.mx/",
    "license" : "AGPL-3",
    "depends" : ["sale","stock","account","board","base"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
                "sale_view.xml",
                    ],
    "installable" : True, # Permite al usuario instalar el Modulo.
    "active" : False,
    # "autoinstall": True, Instalado automaticamente
    #                       cuando se crea una BD
}
