# -*- coding: latin-1 -*-

import sys, os

############################################################################################################
class DicOrdenado :
    def __init__( self ) :
        self.dicc = {}
        self.lista = []
    def nuevo( self, k, pregunta, valor, siCambiable = True ) : # siCambiable = si se puede machacar valor con lo guardado en fichero
        self.lista.append( k )
        # Si no tiene contenido valor, se podrá cambiar
        if not siCambiable :
            siCambiable = len(valor) == 0
        self.dicc[k] = [ pregunta, valor, siCambiable ]
    def __setitem__( self, k, valor ) :
        if k in self.lista :
            self.dicc[k][1] = valor
    def __getitem__( self, k ) :
        try :
            return self.dicc[k][1]
        except :
            sys.exit( 0 )
    def pregunta( self, k ) :
        return self.dicc[k][0]
    def siCambiable( self, k ) :
        return self.dicc[k][2]
    def keys( self ) :
        return self.lista

############################################################################################################
def varExten( dirGuardar, tipo, dicOrden ) :

    # Comprobamos si tenemos datos guardados
    tipo = tipo.replace( ".", "_" ).replace("/", "_").replace("\\", "_")
    datosGuardados = dirGuardar + "/" + tipo + ".varExten"
    if os.path.isfile( datosGuardados ) :
        f = open( datosGuardados, "rb" )
        for linea in f :
            linea = linea.strip()
            li = linea.split( "·" )
            if len(li) == 2 :
                clave,respuesta = li
                if clave in dicOrden.keys() and dicOrden.siCambiable(clave) :
                    dicOrden[clave] = respuesta
        f.close()

    dir = os.path.abspath(dirGuardar + "/../bin/" ) + "\\"

    respuesta = dir + "VarExten.respuesta"
    datos = dir + "VarExten.datos"
    bin = dir + "VarExten.exe"

    # Escribimos el fichero de intercambio
    f = open( datos, "wb" )
    for k in dicOrden.keys() :
        f.write( "%s·%s·%s\r\n"%(k,dicOrden.pregunta(k),dicOrden[k]) )
    f.close()

    # Borramos por si existe el fichero de respuesta
    try :
        os.remove( respuesta )
    except :
        pass

    # Lanzamos el programa
    os.spawnl( os.P_WAIT, bin )

    # Miramos lo recibido
    f = open( respuesta, "rb" )
    siSeguir = False
    for x in f :
        x = x.strip()
        if x :
            clave, valor = x.split( "·" )
            dicOrden[clave] = valor
            siSeguir = True
    f.close

    # Guardamos
    if siSeguir :
        f = open( datosGuardados, "wb" )
        for clave in dicOrden.keys() :
            if dicOrden.siCambiable( clave ) :
                f.write( "%s·%s\r\n"%( clave, dicOrden[clave] ) )
        f.close()

    return siSeguir
############################################################################################################
