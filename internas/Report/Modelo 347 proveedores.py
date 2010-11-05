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
            resp = g.AskYesNoCancel( "Los datos comunes de las cabeceras de CLIENTES y PROVEEDORES no coinciden, � seguimos ?", yes="Si", no="No", cancel="" )
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

# ### Comprobamos primero si est�n las columnas necesarias
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
    dicDatos.nuevo( "APEDEC", "Apellidos y nombre o raz�n social del declarante", FV( "NOMBRE" ) )
    dicDatos.nuevo( "SOPORTE", "Tipo de soporte C si en CDrom o T si transmisi�n telem�tica", "T" )
    dicDatos.nuevo( "TELEREL", "Tel�fono, persona con quien relacionarse", "" )
    dicDatos.nuevo( "APEREL", "Apellidos y nombre, persona con quien relacionarse", "" )
    dicDatos.nuevo( "NUMERO", "N�mero identificativo correspondiente a la declaraci�n", "1" )
    dicDatos.nuevo( "TIPODECL", "Tipo de declaraci�n, C:complementaria S:sustitutiva, en blanco normal", "", False )
    dicDatos.nuevo( "NUMANTERIOR",  "Si declaraci�n complementaria o sustitutiva, n. declaraci�n anterior", "", False )
    dicDatos.nuevo( "NIFREPRE", "NIF del representante legal", FV( "NIF" ) )
    dicDatos.nuevo( "CABPAIS", "Cabecera en la impresi�n que indica el c�digo de pa�s (en blanco, todos=Espa�a)", "" )
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

    # Pa�s
    cabpais = dicDatos[ "CABPAIS" ].strip()
    clavePAIS = None
    if cabpais :
        buspais = cabpais.upper().replace( " ", "" ).replace( ".", "" ).replace( "�", "" )
        num = 1
        numCabPais = 0
        while True :
            cab = "CABECERA.%d"%num
            val = FV( cab, "@@" )
            if val == "@@" :
                break
            val = val.upper().replace( " ", "" ).replace( ".", "" ).replace( "�", "" )
            if val == buspais :
                numCabPais = num
                break
        if numCabPais == 0 :
            Error( "El r�tulo %s de cabecera de impresi�n que contiene el c�digo de pais no existe, as� que no se puede determinar el c�digo de pa�s de cada registro" )
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
            Error( "%s tiene mal el c�digo postal"%d["NOMBRE"] )
        pais = "  "
        if clavePAIS :
            pais = d[ clavePAIS ]
            if pais :
                if not len(pais) == 2 :
                    Error( "%s tiene mal el c�digo del pa�s : %s"%(d["NOMBRE"],pais) )
        d[ "PAIS" ] = pais
        liDatos.append( d )
        total += d["IMPORTE"]

# ### Generamos el fichero

    fich347 = FC( "DESTINO" )
    if os.path.isfile( fich347 ) :
        os.remove( fich347 )
    out347 = clLog( fich347 )

    # Primero : linea del presentador
    # 1 Num�rico TIPO DE REGISTRO.
    out347.esc( "1" )

    # 2-4 Num�rico MODELO DECLARACI�N.
    out347.esc( "347" )

    # 5-8 Num�rico EJERCICIO.
    out347.esc( dicDatos[ "EFISCAL" ] )

    #9-17 Alfanum�rico NIF DEL DECLARANTE.
    out347.escF0( dicDatos[ "NIF" ], 9 )

    # 18-57 Alfanum�rico APELLIDOS Y NOMBRE O RAZ�N SOCIAL DEL DEL DECLARANTE.
    out347.escF( dicDatos[ "APEDEC" ], 40 )

    # 58 Alfab�tico TIPO DE SOPORTE.
    out347.esc( tipoSOPORTE )

    # 59-67 TEL�FONO: Campo num�rico de 9 posiciones.
    out347.escF0( dicDatos[ "TELEREL" ],9 )

    # 68-107 APELLIDOS Y NOMBRE: Se consignar� el primer
    out347.escF( dicDatos[ "APEREL" ], 40 )

    # 108-120 Num�rico NUMERO IDENTIFICATIVO DE LA
    out347.esc( "347" )
    out347.escF0( dicDatos[ "NUMERO" ], 10 )

    # 121-122 Alfab�tico DECLARACION COMPLEMENTARIA O SUSTITUTIVA.
    tipo = dicDatos[ "TIPODECL" ]
    if tipo not in "CD" :
        tipo = " "
    out347.escF( tipo, 2 )

    # 123- 135 Num�rico NUMERO IDENTIFICATIVO DE LA DECLARACI�N ANTERIOR.
    if tipo in "CD" :
        out347.esc( "347" )
        out347.escF0( dicDatos[ "NUMANTERIOR" ], 10 )
    else :
        out347.esc( " "*13 )

    # 136-144 Num�rico NUMERO TOTAL DE PERSONAS Y ENTIDADES.
    out347.escNum0( nr, 9, 0 )

    # 145-159 Num�rico IMPORTE TOTAL DE LAS OPERACIONES.
    out347.escNum0( total, 15, 2 )

    # 160-168 Num�rico NUMERO TOTAL DE INMUEBLES.
    out347.escNum0( 0, 9, 0 )

    # 169-183 Num�rico IMPORTE TOTAL DE LAS OPERACIONES DE ARRENDAMIENTO DE LOCALES DE NEGOCIO.
    out347.escNum0( 0, 15, 0 )

    # 184-390 ------------ BLANCOS
    out347.esc( " "*(390-184+1) )

    # 391-399 Alfanum�rico NIF DEL REPRESENTANTE LEGAL.
    out347.escF0( dicDatos[ "NIFREPRE" ], 9 )

    # 400-487 ------------ BLANCOS
    out347.esc( " "*(487-400+1) )

    # 488-500 Alfanum�rico SELLO ELECTRONICO
    out347.esc( " "*(500-488+1) )

    out347.esc( "\r\n" )

# ### Segundo : registros de los clientes


    for i in range( nr ) :
        dicREG = liDatos[i]

        #1 Num�rico TIPO DE REGISTRO.
        out347.esc( "2" )

        # 2-4 Num�rico MODELO DECLARACI�N.
        out347.esc( "347" )

        # 5-8 Num�rico EJERCICIO.
        out347.esc( dicDatos[ "EFISCAL" ] )

        #9-17 Alfanum�rico NIF DEL DECLARANTE.
        out347.escF0( dicDatos[ "NIF" ], 9 )

        # 18-26 Alfanum�rico NIF DEL DECLARADO.
        out347.escF0( dicREG[ "NIF" ], 9 )

        # 27-35 Alfanum�rico NIF DEL REPRESENTANTE LEGAL.
        out347.esc( " "*9 )

        # 36-75 Alfanum�rico APELLIDOS Y NOMBRE, RAZ�N SOCIAL O
        out347.escF( dicREG[ "NOMBRE" ], 40 )

        # 76 Alfab�tico TIPO DE HOJA.
        out347.esc( "D" )

        # 77-78 C�DIGO PROVINCIA:
        out347.esc( dicREG[ "PROVINCIA" ] )

        # 79-80 C�DIGO PA�S.
        out347.esc( dicREG[ "PAIS" ] )

        # 81 ------------ BLANCOS
        out347.esc( " " )

        # 82 Alfab�tico CLAVE OPERACI�N.
        out347.esc( tipoOP )

        # 83-97 Num�rico IMPORTE DE LAS OPERACIONES.
        out347.escNum0( dicREG[ "IMPORTE"], 15, 2 )

        # 98 Alfab�tico OPERACI�N SEGURO.
        out347.esc( " " )

        # 99 Alfab�tico ARRENDAMIENTO LOCAL NEGOCIO.
        out347.esc( " " )

        # 100-114 Num�rico IMPORTE PERCIBIDO EN MET�LICO.
        out347.escNum0( 0, 15, 2 )

        # 115-129 Num�rico IMPORTE PERCIBIDO POR TRANSMISIONES DE INMUEBLES SUJETAS A IVA.
        out347.escNum0( 0, 15, 2 )

        # 130-500 -------- BLANCOS.
        out347.esc( " "*(500-130+1) )

        out347.esc( "\r\n" )


    out347.cerrar()

    juntar( fich347 )


if __name__ == '__main__':
    Crear347("A")
