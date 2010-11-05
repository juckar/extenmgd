# -*- coding: latin-1 -*-

# Base
import sys, os
sys.path.append( gBase + "/library.zip" )
from jFusion import *
from jDBF import *
import EasyDialogs as g
import VarExten as ve

############################################################################################################
def Error( cMens ) :
    g.Message( cMens, ok= "Terminar" )
    sys.exit()

############################################################################################################
# Llamada para el acceso a las variables enviadas por MGD
# La variable FusionMGD se recibe por defecto del programa que lanza esta rutina
def FV( clave, defecto = "" ) :
    if clave in FusionMGD.dicc :
        return FusionMGD.dicc[clave]
    else :
        return defecto

############################################################################################################
def Crear58() :


    # Leemos los datos
    dicDatos = ve.DicOrdenado()
    dicDatos.nuevo( "NIF_PRESENTADOR", "NIF del presentador", FV("NIF_PRESENTADOR")  )
    dicDatos.nuevo( "SUFIJO_58", "Sufijo", FV("SUFIJO_58") )
    dicDatos.nuevo( "NOMBRE_PRESENTADOR", "Nombre del presentador", FV("NOMBRE_PRESENTADOR") )
    dicDatos.nuevo( "NUMERO_CUENTA", "20 dígitos de la cuenta", FV("NUMERO_CUENTA") )
    dicDatos.nuevo( "NIF_ORDENANTE", "NIF del ordenante", FV("NIF_ORDENANTE") )
    dicDatos.nuevo( "NOMBRE_ORDENANTE", "Nombre del ordenante", FV("NOMBRE_ORDENANTE") )
    dicDatos.nuevo( "CODIGO_INE_58", "Código INE de la Plaza de emisión", FV("CODIGO_INE_19") )
    dicDatos.nuevo( "LOCALIDAD_ORDENANTE", "Localidad del ordenante", FV("LOCALIDAD_ORDENANTE") )
    dicDatos.nuevo( "PROVINCIA_ORDENANTE", "Código provincia de la localidad del ordenante (2 dígitos)", FV("PROVINCIA_ORDENANTE") )
    dicDatos.nuevo( "FECHA_HOY", "Fecha", FV("FECHA_HOY"), False )

    siSeguir = ve.varExten( gBase, "58"+FV("NOMBRE"), dicDatos )
    if not siSeguir :
        return


    # Abrimos el fichero de datos
    dbDatos = clDBF( FV( "FDATOS" ) )

    # Fichero a generar
    fich58 = FV( "DESTINO" )
    if os.path.isfile( fich58 ) :
        os.remove( fich58 )
    out58 = clLog( fich58 )

    # Primero : linea del presentador
    #   Necesitamos el CIF, el sufijo, fecha, nombre, entidad, oficina
    nifPres = dicDatos["NIF_PRESENTADOR"].strip()
    sufijo = dicDatos["SUFIJO_58"].strip()
    fecha = dicDatos["FECHA_HOY"]
    d = fecha.split( "/" )
    if len(d) != 3 :
        d = fecha.split( "-" )
        if len(d) != 3 :
            Error( "Falta la fecha" )
    nombre = dicDatos["NOMBRE_PRESENTADOR"].strip()

    cNumeroCuenta = dicDatos["NUMERO_CUENTA"].strip()
    if len(cNumeroCuenta) != 20 :
        Error( "El número de cuenta ha de tener 20 dígitos. Si hemos asociado un banco al vencimiento, es necesario añadir los 20 dígitos a la información del banco en el campo Número de cuenta." )

    entidad = cNumeroCuenta[:4]
    oficina = cNumeroCuenta[4:8]

    out58.esc( "5170" )
    out58.escF0( nifPres, 9 )
    out58.escF( sufijo, 3 )
    out58.esc( "%02d%02d%02d"%(int(d[0]),int(d[1]),int(d[2])%100 ) )
    out58.esc( " "*6 )
    out58.escF( nombre, 40 )
    out58.esc( " "*20 )
    out58.escF( entidad, 4 )
    out58.escF( oficina, 4 )
    out58.linea( " "*66 )

    # Segundo : linea del ordenante
    #   Necesitamos el CIF, el sufijo, fecha, nombre, entidad, oficina
    nif = dicDatos["NIF_ORDENANTE"]
    nombre = dicDatos["NOMBRE_ORDENANTE"]
    dc = cNumeroCuenta[8:10]
    cuenta = cNumeroCuenta[10:]
    codINE = dicDatos["CODIGO_INE_58"]

    out58.esc( "5370" )
    out58.escF0( nif, 9 )
    out58.escF( sufijo, 3 )
    out58.esc( "%02d%02d%02d"%(int(d[0]),int(d[1]),int(d[2])%100 ) )
    out58.esc( "%02d%02d%02d"%(int(d[0]),int(d[1]),int(d[2])%100 ) ) # 20/11/88
    out58.escF( nombre, 40 )
    out58.escF( entidad, 4 )
    out58.escF( oficina, 4 )
    out58.escF( dc, 2 )
    out58.escF( cuenta, 10 )
    out58.esc( " "*8+ "01" + " "*52 )
    out58.escF( codINE, 9 )
    out58.linea( " "*3 )

# ### Tercero : registros de los clientes

    localidad = dicDatos["LOCALIDAD_ORDENANTE"]
    provincia = dicDatos["PROVINCIA_ORDENANTE"]

    nr = dbDatos.numRegistros

    suma = 0.00

    for i in range( nr ) :
        dbDatos.goto( i + 1)

        # Primer registro
        out58.esc( "5670" )
        out58.escF0( nif, 9 )
        out58.escF( sufijo, 3 )
        out58.escF0( dbDatos.registro["CUENTA"], 12 )
        out58.escF( dbDatos.registro["NOMBRE"], 40 )
        out58.escF( dbDatos.registro["BANCO_DIG"], 20 )
        pendiente = dbDatos.registro["IMPORTE"]
        suma += pendiente
        out58.escNum0( pendiente, 10, 2 )
        out58.esc( "0"*16 )
        out58.escF( dbDatos.registro["TEXTO"], 40 )
        dFecha = dbDatos.registro["FVTO"]
        out58.esc( "%02d%02d%02d" % ( dFecha.dia, dFecha.mes, dFecha.eje%100 ) )
        out58.linea( " "*2 )

        # Segundo registro
        out58.esc( "5676" )
        out58.escF0( nif, 9 )
        out58.escF( sufijo, 3 )
        out58.escF0( dbDatos.registro["CUENTA"], 12 )
        out58.escF( dbDatos.registro["DOMICILIO"], 40 )
        out58.escF( dbDatos.registro["LOCALIDAD"], 35 )
        out58.escF( dbDatos.registro["COD_POSTAL"], 5 )
        out58.escF( localidad, 38 )
        out58.escF( provincia, 2 )
        d = dbDatos.registro["FEMISION"]
        out58.esc( "%02d%02d%02d"%(d.dia,d.mes,(d.eje)%100 ) )
        out58.linea( " "*8 )

# ### Cuarto : REGISTRO TOTAL DEL CLIENTE ORDENANTE
    out58.esc( "5870" )
    out58.escF0( nif, 9 )
    out58.escF( sufijo, 3 )
    out58.esc( " "*72 )
    out58.escNum0( suma, 10, 2 )
    out58.esc( " "*6 )
    out58.esc( "%010d"%( nr,) )
    out58.esc( "%010d"%( 1+ nr*2 + 1 ,) )
    out58.linea( " "*38 )

# ### Quinto : REGISTRO TOTAL GENERAL
    out58.esc( "5970" )
    out58.escF0( nifPres, 9 )
    out58.escF( sufijo, 3 )
    out58.esc( " "*52 ) # 20/11/08
    out58.esc( "%04d"%( 1,) ) # 9/12/08 # 20/11/08
    out58.esc( " "*16 ) # 20/11/08
    out58.escNum0( suma, 10, 2 )
    out58.esc( " "*6 )
    out58.esc( "%010d"%( nr,) )
    out58.esc( "%010d"%( 1+ nr*2 + 1 + 2,) )
    out58.linea( " "*38 )


    out58.cerrar()


if __name__ == '__main__':
    Crear58()
