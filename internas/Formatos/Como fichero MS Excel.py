# -*- coding: latin-1 -*-

import sys, os

sys.path.append( gBase + "/library.zip" )

import pyXLWriter as xl

from jFusion import *
from jDBF import *

############################################################################################################
def columna( col ) :
    if col > 26 :
        c = chr(64+(col/26)) + chr(65+(col%26))
    else :
        c = chr(64+col)
    return c
############################################################################################################
def celda( fila, col ) :
    c = columna(col) + "%s"
    return c%fila

############################################################################################################
def CrearXLS() :

    FC = FusionMGD.clave # Forma abreviada de llamada a la función

    # Abrimos el fichero de datos
    dbDatos = clDBF( FC( "FDATOS" ) )
    nr = dbDatos.numRegistros

    # Miramos los campos y creamos una lista con los nombres
    lc = []
    nc = len(dbDatos.campos)
    for i in range(nc) :
        lc.append( dbDatos.campos[i][0] )

    # Creamos el fichero
    xls = FC( "DESTINO" )
    if os.path.isfile( xls ) :
        os.remove( xls )
    workbook = xl.Writer( xls )
    worksheet = workbook.add_worksheet('Datos')

    # Formatos
    cab_format = workbook.add_format(bold = 1, color = 'blue', size = 10, align = "center", )
    aliI = workbook.add_format( align = "left", )
    aliD = workbook.add_format( align = "right", )
    aliC = workbook.add_format( align = "center", )
    date_format = workbook.add_format( align = "center" )
    date_format.set_num_format( "dd/mm/yyyy" )
    num_format = []
    for i in range( nc-1 ) :
        col = i + 1
        tipo = dbDatos.campos[i][1]
        fm = None
        if tipo == "N" :
            decimales = int(FC( "DECIMALES.%s"%col ))
            fm = workbook.add_format(  )
            cfm = "##,##0"
            if decimales > 0 :
                cfm = cfm + "." + "0"*decimales
            fm.set_num_format( cfm )
        num_format.append( fm )

    # Cabeceras
    for i in range( nc-1 ) :
        col = i + 1
        alin = FC( "ALINEACION.%s"%col )
        fm = aliD
        if alin == "I" :
            fm  = aliI
        elif alin == "C" :
            fm = aliC
        worksheet.set_column( (i,i), width=dbDatos.campos[i][2]+2, format=fm )
        worksheet.write( (0,i), FC( "CABECERA.%s"%col ), cab_format )

    # Datos
    for i in range( nr ) :
        dbDatos.goto( i + 1)
        nivel = dbDatos.registro["NIVEL"]
        if nivel > 1 :
            hid = 1
        else :
            hid = 0

        worksheet.set_row(i+1, hidden=hid, level=nivel-1)

        for j in range( nc-1 ) :
            dato = dbDatos.registro[lc[j]]
            tipo = dbDatos.campos[j][1]
            if tipo == "D" :
                if dato.eje > 0 :
                    worksheet.write_date(( i + 1, j ), dato.datetime(), date_format)
            elif tipo == "N" :
                if dato != 0 :
                    worksheet.write( ( i + 1, j ), dato, num_format[j] )
            elif tipo == "C" :
                worksheet.write_string( ( i + 1, j ), dato )
            else :
                worksheet.write( ( i + 1, j ), dato )

    dbDatos.cerrar()

    workbook.close()

if __name__ == '__main__':
    try :
        CrearXLS()
    except :
        sys.exit(0)
