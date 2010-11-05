# -*- coding: latin-1 -*-

# Base
import sys, os

sys.path.append( gBase + "/library.zip" )
from jFusion import *
from jDBF import *
import EasyDialogs as g
import VarExten as ve

############################################################################################################
def juntar( cFich ) :
    resp = g.AskYesNoCancel( "Unimos el fichero creado al de CLIENTES si se ha generado anteriormente, y creamos uno conjunto", yes="Si", no="No", cancel="" )
    if resp != 1 :
        return

    fichCli = g.AskFileForOpen( "Indica el fichero generado anteriormente de CLIENTES", defaultLocation= os.path.split(cFich)[0] )

    if fichCli and fichCli != cFich :

        fCli = open( fichCli, "rb" )
        liCli = [ linea for linea in fCli ]
        fCli.close()

        fProv = open( cFich, "rb" )
        liProv = [ linea for linea in fProv ]
        fProv.close()

        cabCli = liCli[0]
        cabProv = liProv[0]
        nr = int(cabCli[135:144]) + int(cabProv[135:144])

        total = int(cabCli[144:159]) + int(cabProv[144:159])

        if cabProv[:135] != cabCli[:135] or cabProv[159:] != cabCli[159:] :
            resp = g.AskYesNoCancel( "Los datos comunes de las cabeceras de CLIENTES y PROVEEDORES no coinciden, ¿ seguimos ?", yes="Si", no="No", cancel="" )
            if resp != 1 :
                return


        cab = cabProv[:135] + "%09d%015d"%(nr,total) + cabProv[159:]


        fichDestino = g.AskFileForSave( "Indica el nombre del fichero CONJUNTO a generar", "Listado conjunto.347", defaultLocation= os.path.split(cFich)[0] )
        if fichDestino :

            q = open( fichDestino, "wb" )

            q.write( cab )

            del( liCli[0] )
            for linea in liCli :
                q.write( linea )

            del( liProv[0] )
            for linea in liProv :
                q.write( linea )

            q.close()


############################################################################################################
def Error( cMens ) :
    g.Message( cMens, ok= "Terminar" )
    sys.exit()

############################################################################################################
def Crear347(tipoOP) :
    # clientes = B, proveedores = A

    FC = FusionMGD.clave # Forma abreviada de llamada para el acceso a las variables enviadas por MGD
    Fdicc = FusionMGD.dicc # Diccionario de datos
    def FV( clave, defecto = "" ) :
        if clave in FusionMGD.dicc :
            return FusionMGD.dicc[clave]
        else :
            return defecto

# ### Comprobamos primero si están las columnas necesarias
    # Abrimos el fichero de datos
    dbDatos = clDBF( FC( "FDATOS" ) )

    # Miramos los campos y creamos una lista con los nombres
    lc = []
    nc = len(dbDatos.campos)
    for i in range(nc) :
        lc.append( dbDatos.campos[i][0] )

    # Campos necesarios
    lcn = ['BRUTO', 'NIF', 'NOMBRE', 'COD_POSTAL']
    for campo in lcn :
        if campo not in lc :
            Error( "Falta de indicar la columna %s"%campo )



# ### Leemos las variables

    fecha = FC( "FECHA_HOY" ) #23/10/2007
    eje = fecha[6:].strip()
    base = int(eje)
    if len(eje) == 2 :
        eje = "20" + eje
    dicDatos = ve.DicOrdenado()
    dicDatos.nuevo( "EFISCAL", "Ejercicio fiscal", str(int(eje)-1), False )
    dicDatos.nuevo( "NIF", "NIF del declarante", FV( "NIF" ) )
    dicDatos.nuevo( "APEDEC", "Apellidos y nombre o razón social del declarante", FV( "NOMBRE" ) )
    dicDatos.nuevo( "SOPORTE", "Tipo de soporte C si en CDrom o T si transmisión telemática", "T" )
    dicDatos.nuevo( "TELEREL", "Teléfono, persona con quien relacionarse", "" )
    dicDatos.nuevo( "APEREL", "Apellidos y nombre, persona con quien relacionarse", "" )
    dicDatos.nuevo( "NUMERO", "Número identificativo correspondiente a la declaración", "1" )
    dicDatos.nuevo( "TIPODECL", "Tipo de declaración, C:complementaria S:sustitutiva, en blanco normal", "", False )
    dicDatos.nuevo( "NUMANTERIOR",  "Si declaración complementaria o sustitutiva, n. declaración anterior", "", False )
    dicDatos.nuevo( "NIFREPRE", "NIF del representante legal", FV( "NIF" ) )
    dicDatos.nuevo( "CABPAIS", "Cabecera en la impresión que indica el código de país (en blanco, todos=España)", "" )
    siSeguir = ve.varExten( gBase, "347"+FV("NOMBRE"), dicDatos )
    if not siSeguir :
        return

    tipoSOPORTE = dicDatos["SOPORTE"].upper().strip()
    if not tipoSOPORTE or tipoSOPORTE not in "CT" :
        Error( "El tipo de soporte tiene que ser T o C." )


# ### Comprobamos que en todas los registros disponemos de NIF y provincia = cod_postal[:2]
    # a la vez calculamos el importe total
    total = 0.0
    nr = dbDatos.numRegistros
    liDatos = []

    # País
    cabpais = dicDatos[ "CABPAIS" ].strip()
    clavePAIS = None
    if cabpais :
        buspais = cabpais.upper().replace( " ", "" ).replace( ".", "" ).replace( "º", "" )
        num = 1
        numCabPais = 0
        while True :
            cab = "CABECERA.%d"%num
            val = FV( cab, "@@" )
            if val == "@@" :
                break
            val = val.upper().replace( " ", "" ).replace( ".", "" ).replace( "º", "" )
            if val == buspais :
                numCabPais = num
                break
        if numCabPais == 0 :
            Error( "El rótulo %s de cabecera de impresión que contiene el código de pais no existe, así que no se puede determinar el código de país de cada registro" )
        clavePAIS = lc[numCabPais-1]

    for i in range( nr ) :
        dbDatos.goto( i + 1)
        d = {}
        d["IMPORTE"] = dbDatos.registro["BRUTO"]
        d["NIF"] = dbDatos.registro["NIF"].strip()
        d["NOMBRE"] = dbDatos.registro["NOMBRE"]
        if not d["NIF"] :
            Error( "%s no tiene NIF"%d["NOMBRE"] )
        cod_postal = dbDatos.registro["COD_POSTAL"].strip()
        d["PROVINCIA"] = provincia = cod_postal[:2]
        if not provincia or not provincia.isdigit() or int(provincia) == 0 :
            Error( "%s tiene mal el código postal"%d["NOMBRE"] )
        pais = "  "
        if clavePAIS :
            pais = d[ clavePAIS ]
            if pais :
                if not len(pais) == 2 :
                    Error( "%s tiene mal el código del país : %s"%(d["NOMBRE"],pais) )
        d[ "PAIS" ] = pais
        liDatos.append( d )
        total += d["IMPORTE"]

# ### Generamos el fichero

    fich347 = FC( "DESTINO" )
    if os.path.isfile( fich347 ) :
        os.remove( fich347 )
    out347 = clLog( fich347 )

    # Primero : linea del presentador
    # 1 Numérico TIPO DE REGISTRO.
    out347.esc( "1" )

    # 2-4 Numérico MODELO DECLARACIÓN.
    out347.esc( "347" )

    # 5-8 Numérico EJERCICIO.
    out347.esc( dicDatos[ "EFISCAL" ] )

    #9-17 Alfanumérico NIF DEL DECLARANTE.
    out347.escF0( dicDatos[ "NIF" ], 9 )

    # 18-57 Alfanumérico APELLIDOS Y NOMBRE O RAZÓN SOCIAL DEL DEL DECLARANTE.
    out347.escF( dicDatos[ "APEDEC" ], 40 )

    # 58 Alfabético TIPO DE SOPORTE.
    out347.esc( tipoSOPORTE )

    # 59-67 TELÉFONO: Campo numérico de 9 posiciones.
    out347.escF0( dicDatos[ "TELEREL" ],9 )

    # 68-107 APELLIDOS Y NOMBRE: Se consignará el primer
    out347.escF( dicDatos[ "APEREL" ], 40 )

    # 108-120 Numérico NUMERO IDENTIFICATIVO DE LA
    out347.esc( "347" )
    out347.escF0( dicDatos[ "NUMERO" ], 10 )

    # 121-122 Alfabético DECLARACION COMPLEMENTARIA O SUSTITUTIVA.
    tipo = dicDatos[ "TIPODECL" ]
    if tipo not in "CD" :
        tipo = " "
    out347.escF( tipo, 2 )

    # 123- 135 Numérico NUMERO IDENTIFICATIVO DE LA DECLARACIÓN ANTERIOR.
    if tipo in "CD" :
        out347.esc( "347" )
        out347.escF0( dicDatos[ "NUMANTERIOR" ], 10 )
    else :
        out347.esc( " "*13 )

    # 136-144 Numérico NUMERO TOTAL DE PERSONAS Y ENTIDADES.
    out347.escNum0( nr, 9, 0 )

    # 145-159 Numérico IMPORTE TOTAL DE LAS OPERACIONES.
    out347.escNum0( total, 15, 2 )

    # 160-168 Numérico NUMERO TOTAL DE INMUEBLES.
    out347.escNum0( 0, 9, 0 )

    # 169-183 Numérico IMPORTE TOTAL DE LAS OPERACIONES DE ARRENDAMIENTO DE LOCALES DE NEGOCIO.
    out347.escNum0( 0, 15, 0 )

    # 184-390 ------------ BLANCOS
    out347.esc( " "*(390-184+1) )

    # 391-399 Alfanumérico NIF DEL REPRESENTANTE LEGAL.
    out347.escF0( dicDatos[ "NIFREPRE" ], 9 )

    # 400-487 ------------ BLANCOS
    out347.esc( " "*(487-400+1) )

    # 488-500 Alfanumérico SELLO ELECTRONICO
    out347.esc( " "*(500-488+1) )

    out347.esc( "\r\n" )

# ### Segundo : registros de los clientes


    for i in range( nr ) :
        dicREG = liDatos[i]

        #1 Numérico TIPO DE REGISTRO.
        out347.esc( "2" )

        # 2-4 Numérico MODELO DECLARACIÓN.
        out347.esc( "347" )

        # 5-8 Numérico EJERCICIO.
        out347.esc( dicDatos[ "EFISCAL" ] )

        #9-17 Alfanumérico NIF DEL DECLARANTE.
        out347.escF0( dicDatos[ "NIF" ], 9 )

        # 18-26 Alfanumérico NIF DEL DECLARADO.
        out347.escF0( dicREG[ "NIF" ], 9 )

        # 27-35 Alfanumérico NIF DEL REPRESENTANTE LEGAL.
        out347.esc( " "*9 )

        # 36-75 Alfanumérico APELLIDOS Y NOMBRE, RAZÓN SOCIAL O
        out347.escF( dicREG[ "NOMBRE" ], 40 )

        # 76 Alfabético TIPO DE HOJA.
        out347.esc( "D" )

        # 77-78 CÓDIGO PROVINCIA:
        out347.esc( dicREG[ "PROVINCIA" ] )

        # 79-80 CÓDIGO PAÍS.
        out347.esc( dicREG[ "PAIS" ] )

        # 81 ------------ BLANCOS
        out347.esc( " " )

        # 82 Alfabético CLAVE OPERACIÓN.
        out347.esc( tipoOP )

        # 83-97 Numérico IMPORTE DE LAS OPERACIONES.
        out347.escNum0( dicREG[ "IMPORTE"], 15, 2 )

        # 98 Alfabético OPERACIÓN SEGURO.
        out347.esc( " " )

        # 99 Alfabético ARRENDAMIENTO LOCAL NEGOCIO.
        out347.esc( " " )

        # 100-114 Numérico IMPORTE PERCIBIDO EN METÁLICO.
        out347.escNum0( 0, 15, 2 )

        # 115-129 Numérico IMPORTE PERCIBIDO POR TRANSMISIONES DE INMUEBLES SUJETAS A IVA.
        out347.escNum0( 0, 15, 2 )

        # 130-500 -------- BLANCOS.
        out347.esc( " "*(500-130+1) )

        out347.esc( "\r\n" )


    out347.cerrar()

    juntar( fich347 )


if __name__ == '__main__':
    Crear347("A")
