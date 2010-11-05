# -*- coding: latin-1 -*-

import sys, os


sys.path.append( gBase + "/library.zip" )
import pyXLWriter as xl

from jFusion import *
from jDBF import *

############################################################################################################
def long_string(str):
    limit = 255
    # Return short strings
    if len(str) <= limit:
        return str
    # Split the line at word boundaries where possible

    segments = [str[0:limit]]
    i_prev = 0
    for i in xrange(limit, len(str), limit):
        segments.append(str[i_prev:i])
        i_prev=i
    # Join the string back together with quotes and Excel concatenation
    str = string.join(segments, '"&"')
    # Add formatting to convert the string to a formula string
    return '="' + str + '"'
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
    dAlin = { "I":"left", "D":"right", "C":"center" }
    date_format = None
    num_format = []
    for i in range( nc ) :
        col = i + 1
        tipo = dbDatos.campos[i][1]
        fm = None
        if tipo == "N" :
            puntos = FC( "PUNTOS.%s"%col )
            decimales = int(FC( "DECIMALES.%s"%col ))
            cfm = "#"
            if puntos == "S" :
                cfm = cfm + "#,##0"
            if decimales > 0 :
                cfm = cfm + "." + "0"*decimales
            alin = FC( "ALINEACION.%s"%col )
            if alin not in dAlin :
                alin = "D"
            fm = workbook.add_format( align = dAlin[alin], num_format = cfm, )
        num_format.append( fm )

    # Cabeceras
    cab_format = workbook.add_format(bold = 1, color = 'blue', size = 12, align = "center", )
    for i in range( nc ) :
        col = i + 1
        alin = FC( "ALINEACION.%s"%col )
        if alin not in dAlin :
            alin = "I"
        fm = workbook.add_format( align = dAlin[alin],  )
        worksheet.set_column( (i,i), width=dbDatos.campos[i][2]+2, format=fm )
        worksheet.write( (0,i), FC( "CABECERA.%s"%col ), cab_format )

    # Datos
    for i in range( nr ) :
        dbDatos.goto( i + 1)
        for j in range( nc ) :
            dato = dbDatos.registro[lc[j]]
            tipo = dbDatos.campos[j][1]
            if tipo == "D" :
                if dato.eje > 0 :
                    if date_format is None :
                        date_format = workbook.add_format( num_format="dd/mm/yyyy", align = "center", )
                    worksheet.write_date(( i + 1, j ), dato.datetime(), date_format)
            elif tipo == "N" :
                if dato != 0 :
                    worksheet.write( ( i + 1, j ), dato, num_format[j] )
            elif tipo == "C" or tipo == "M" :
                worksheet.write_string( ( i + 1, j ), long_string(dato) )
            else :
                worksheet.write( ( i + 1, j ), dato )

    # Sumas
    for i in range( nc ) :
        col = i + 1
        tipo = dbDatos.campos[i][1]
        if tipo == "N" :
            sumar = FC( "SUMAR.%s"%col )
            if sumar == "S" :
                worksheet.write( ( 2 + nr, i ), '=SUM('+ celda( 2, col ) + ':' + celda( nr+1, col ) + ')', num_format[i] )


    dbDatos.cerrar()

    workbook.close()


if __name__ == '__main__':
    try :
        CrearXLS()
    except :
        sys.exit(0)
