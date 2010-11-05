# -*- coding: latin-1 -*-

import sys, os


sys.path.append( gBase + "/library.zip" )
import csv

from jFusion import *
from jDBF import *


############################################################################################################
def CrearCSV() :

    FC = FusionMGD.clave # Forma abreviada de llamada a la función

    # Abrimos el fichero de datos
    dbDatos = clDBF( FC( "FDATOS" ) )
    nr = dbDatos.numRegistros


    # Miramos los campos y creamos una lista con los nombres
    lc = []
    nc = len(dbDatos.campos)
    for i in range(nc) :
        lc.append( dbDatos.campos[i][0] )


    # Preparamos los datos
    liDatos = []

    # Cabecera
    liFila = []
    for i in range( nc ) :
        col = i + 1
        liFila.append( FC( "CABECERA.%s"%col ) )
    liDatos.append(liFila)

    # Datos
    for i in range( nr ) :
        dbDatos.goto( i + 1)
        liFila = []
        for j in range( nc ) :
            dato = dbDatos.registro[lc[j]]
            tipo = dbDatos.campos[j][1]

            if tipo == "D" :
                dato = str(dato)
            liFila.append( dato )
        liDatos.append(liFila)
    dbDatos.cerrar()


    # Creamos el fichero
    fd = FC( "DESTINO" )
    if os.path.isfile( fd ) :
        os.remove( fd )

    writer = csv.writer(open(fd, "wb"), delimiter=';')
    writer.writerows(liDatos)


if __name__ == '__main__':
    try :
        CrearCSV()
    except :
        sys.exit(0)
