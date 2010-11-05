# -*- coding: latin-1 -*-

import sys, os


sys.path.append( gBase + "/library.zip" )

from jFusion import *

# --------------------------------------------------------------------------------------------------------------------------
import csv



# --------------------------------------------------------------------------------------------------------------------------
def control() :

    FC = FusionMGD.clave # Forma abreviada de llamada a la función

    fichCSV = FC( "FICHCSV" )

    fichResp = FC( "FRESP" )

    separador = FC( "SEPARADOR" )
    cadSEP = FC( "CADSEP" )
    saltoLinea = FC( "SALTOLINEA" )

    csvfile = open(fichCSV)
    d=csvfile.read(1024)
    n = d.find( "\n" )
    if n :
        d = d[:n]
    nc = d.count( "," )
    sep = "," if d.count( "," ) else ";"
    csvfile.seek(0)
    reader = csv.reader(csvfile, delimiter=sep)
    q = open( fichResp, "wb" )
    for row in reader :
        c = ""
        for x in row :
            c += x.replace( separador, cadSEP ).replace( "\n", saltoLinea ) + separador
        q.write( c[:-1] + "\r\n" )
    q.close()
    csvfile.close()

# --------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    control()

