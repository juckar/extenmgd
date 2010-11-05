# -*- coding: latin-1 -*-
import sys, os

sys.path.append( gBase + "/library.zip" )

from jFusion import *
from jFechas import *
from pyExcelerator import *

############################################################################################################
def CrearMGD() :

    reload( sys )
    sys.setdefaultencoding('latin-1')

    FC = FusionMGD.clave # Forma abreviada de llamada a la función, que nos proporciona los parámetros indicados en el programa

    # Determinamos el fichero XLS
    cXLS = FC( "FDATOS" )

    # Creamos el fichero TXT
    cTXT = FC( "DESTINO" )
    if os.path.isfile( cTXT ) :
        os.remove( cTXT )
    fTXT = open( cTXT, "wb" )

    # Desde qué línea empezamos
    nDesde = int(FC( "DESDELINEA" ))-1

    # Separador
    cSeparador = "·"

    # Miramos todas las hojas
    for sheet_name, values in parse_xls(fname):

        keys = values.keys()

        rows    = []
        cols    = []
        for key in keys:
            row, col = key
            if not col in cols: cols.append(col)
            if not row in rows: rows.append(row)

        try:    n_rows = max(rows)
        except: continue
        n_cols = max(cols)


        for row in range(n_rows+1):
            if row < nDesde :
                continue

            cLinea = ""
            for col in range(n_cols+1):
                try :
                    cCelda = str(values[(row, col)])
                except:
                    cCelda = ""
                if cCelda.find( cSeparador ) != -1 : cCelda = cCelda.replace( cSeparador, "." )
                cLinea = cLinea + cCelda + cSeparador

            fTXT.write( cLinea[:-1] + "\r\n" )

    # Cerramos el fichero
    fTXT.close()

if __name__ == '__main__':
    try :
        CrearMGD()
    except :
        sys.exit(0)
