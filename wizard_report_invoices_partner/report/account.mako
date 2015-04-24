<html>
<head>
    <style type="text/css">
            ${css}
        </style>
    <title>Reporte-Consulta-Facturas.pdf</title>
    <meta charset="UTF-8">
</head>
<body>
    %for o in objects:
        <table width="100%" >
            <tr>
              <td >
                CONSULTA DE VENTAS POR CLIENTE 
              </td>
              </tr>
              <tr>
              <td >
                Cliente: ${o.partner_id.name or ''}

              </td>
              <td >
                Fecha Inicio: ${o.start_date or ''}

              </td>
              <td >
                Fecha Fin: ${o.end_date or ''}

              </td>
            </tr>
          </table>
          <table width="100%" >
            <tr>
             
              <td >
                Fecha Inicio: ${o.start_date or ''}

              </td>
              <td >
                Fecha Fin: ${o.end_date or ''}

              </td>
            </tr>
          </table>

          <table width="100%"  style="text-align: center">
            <tr>
              <td style="text-align: center">
                PRODUCTO
              </td>
              <td style="text-align: center">
                DESCRIPCION

              </td>
              <td style="text-align: center">
                CANTIDAD

              </td>
              <td style="text-align: center">
                TOTAL

              </td>
            </tr>
          </table>

          %for line in o.report_lines:
          <table width="100%"  style="text-align: center">
            <tr>
              <td style="text-align: center">
                ${line.product_id.name or ''}
              </td>
              <td style="text-align: center">
                ${line.name or ''}

              </td>
              <td style="text-align: center">
                ${line.qty or ''}

              </td>
              <td style="text-align: center">
                ${line.amount_total or ''}

              </td>
            </tr>
          </table>
          %endfor

  %endfor
</body>
</html>