<html>
<head>
    <style type="text/css">
            ${css}
        </style>
    <title>Factura-Mako.pdf</title>
    <meta charset="UTF-8">
</head>
<body>
    %for o in objects:
        <table width="100%" >
            <tr>
              <td >
                REPORTE FACTURA ${o.number or ''}
              </td>
              </tr>
              <tr>
              <td >
                Cliente: ${o.partner_id.name or ''} 
                  RFC: ${o.partner_id.vat.replace('MX','') if o.partner_id.vat else ''}

              </td>
            </tr>
          </table>

          <table width="100%"  style="text-align: center">
            <tr>
              <td style="text-align: center">
                PRODUCTO
              </td>
              <td style="text-align: center">
                PRECIO

              </td>
              <td style="text-align: center">
                CANTIDAD

              </td>
              <td style="text-align: center">
                TOTAL

              </td>
            </tr>
          </table>

          %for line in o.invoice_line:
          <table width="100%"  style="text-align: center">
            <tr>
              <td style="text-align: center">
                ${line.product_id.name or ''}
              </td>
              <td style="text-align: center">
                ${line.price_unit or ''}

              </td>
              <td style="text-align: center">
                ${line.quantity or ''}

              </td>
              <td style="text-align: center">
                ${line.price_subtotal or ''}

              </td>
            </tr>
          </table>
          %endfor

  %endfor
</body>
</html>