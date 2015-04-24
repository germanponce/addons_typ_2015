# -*- encoding: utf-8 -*-

{
    'name': 'Asistente de Consulta de Facturas por Cliente',
    'version': '1',
    "author" : "Argil C.",
    "category" : "TyP",
    'description': """

        Recibe 3 Parametros:
        - Cliente.
        - Fecha Inicial
        - Fecha Final

        Opcional:
            - No Imprimir PDF. Muestra el Resultado de la Consulta en una Vista de OpenERP.

    """,
    "website" : "http://www.argil.mx/",
    "license" : "AGPL-3",
    "depends" : ["account","report_webkit"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
                "wizard_export_view.xml",
                "wizard_view.xml",
                "report/account_report.xml",
                "account_report_wizard_view.xml",
                'data.xml',
                    ],
    "installable" : True, # Permite al usuario instalar el Modulo.
    "active" : False,
    # "autoinstall": True, Instalado automaticamente
    #                       cuando se crea una BD
}
