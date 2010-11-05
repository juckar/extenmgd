# -*- coding: latin-1 -*-

import sys, os

sys.path.append( gBase + "/library.zip" )

import pyXLWriter as xl

from jFusion import *
from jDBF import *

############################################################################################################
def CrearXLS() :

    FC = FusionMGD.clave # Forma abreviada de llamada a la función

    # Abrimos el fichero de datos
    dbDatos = clDBF( FC( "FDATOS" ) )
    nr = dbDatos.numRegistros


    # Columnas : clave COLUMNAS contiene sólo las que son de importes, le sumamos la de texto
    nc = int(FC( "COLUMNAS" )) + 1
    lc = []
    for i in range(nc) :
        lc.append( dbDatos.campos[i][0] )

    # Creamos el fichero Excel
    xls = FC( "DESTINO" )
    if os.path.isfile( xls ) :
        os.remove( xls )
    workbook = xl.Writer( xls )
    worksheet = workbook.add_worksheet('Datos')

    # Formatos
    cab_format = workbook.add_format(bold = 1, color = 'blue', size = 10, align = "center", )
    tit_format = workbook.add_format(bold = 1, color = 'navy', size = 18, align = "center", )
    txt_format = {}
    diccAlin = {}
    diccAlin[ "I" ] = "left"
    diccAlin[ "D" ] = "right"
    diccAlin[ "C" ] = "center"
    num_format = {}

    # Título
    worksheet.write( (0,0), FC( "TITULO" ) , tit_format )
    fila = 3

    # Con ceros
    siCeros = FC( "CONCEROS" ) == "S"

    # Cabeceras
    for i in range( nc ) :
        col = i + 1
        worksheet.set_column( (i,i), width=dbDatos.campos[i][2]+2 )
        worksheet.write( (fila,i), FC( "CABECERA.%s"%col ), cab_format )
    fila += 1


    # Datos
    for i in range( nr ) :
        dbDatos.goto( i + 1)

        # Si es cambio de cabecera la ponemos
        if dbDatos.registro["CAMBIOCAB"] :
            dato = dbDatos.registro[lc[0]]
            dato = dato.replace( "NUEVA CABECERA: ", "" ) #Eliminamos "NUEVA CABECERA: "
            fila += 1 # Dejamos una linea en blanco
            worksheet.write( (fila,0), dato, cab_format )
            for j in range( 1, nc ) :
                col = j + 1
                worksheet.write( (fila,j), FC( "CABECERA.%s"%col ), cab_format )
            fila += 1
            continue

        # si es negrita se usa para todos los campos
        negrita = dbDatos.registro["NEGRITA"]

        # Formato de texto
        alin_txt = dbDatos.registro["ALIN_TXT"]
        t = (alin_txt,negrita)
        fmt = None
        if t in txt_format :
            fmt = txt_format[t]
        else :
            fmt = workbook.add_format( align = diccAlin[alin_txt], bold = negrita )
            txt_format[t]  = fmt
        margen_txt = dbDatos.registro["MARGEN_TXT"]

        # Formato de números
        decimales = int(dbDatos.registro["DECIMALES"])
        t = (decimales,negrita)
        fm = None
        if t in num_format :
            fm = num_format[t]
        else :
            fm = workbook.add_format( bold = negrita, )
            cfm = "##,##0"
            if decimales > 0 :
                cfm = cfm + "." + "0"*decimales
            fm.set_num_format( cfm )
            num_format[t] = fm

        # Escribimos todos los campos el primero = texto y el resto = números
        for j in range( nc ) :
            dato = dbDatos.registro[lc[j]]
            if j == 0 :
                worksheet.write_string( ( fila, j ), " "*margen_txt + dato, fmt )
            else :
                if siCeros or dato != 0 :
                    worksheet.write( ( fila, j ), dato, fm )

        # Cambio de fila
        fila += 1


    dbDatos.cerrar()
    workbook.close()


if __name__ == '__main__':
    try :
        CrearXLS()
    except :
        sys.exit(0)
