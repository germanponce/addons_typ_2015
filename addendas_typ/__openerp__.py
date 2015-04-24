# -*- encoding: utf-8 -*-

{
    'name': 'Asistente de Generacion de Addendas',
    'version': '1',
    "author" : "Argil C.",
    "category" : "TyP",
    'description': """

        Asistente para generar Addendas

    """,
    "website" : "http://www.argil.mx/",
    "license" : "AGPL-3",
    "depends" : ["account",
            "l10n_mx_facturae_base",
            "l10n_mx_facturae_pac_sf",
            "l10n_mx_ir_attachment_facturae",
            "adenda_xml_femsa_soriana",
                ],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
                "wizard_addenda_view.xml",
                    ],
    "installable" : True, # Permite al usuario instalar el Modulo.
    "active" : False,
    # "autoinstall": True, Instalado automaticamente
    #                       cuando se crea una BD
}
