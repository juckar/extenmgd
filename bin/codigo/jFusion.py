# -*- coding: latin-1 -*-

from jDBF import *
import os, sys

class clFusion :
    """Lee completamente el fichero de fusión lo que permite luego buscar claves"""
    def __init__( self, cFichero ) :
        db = clDBF( cFichero )
        nr = db.numRegistros
        self.dicc = {}
        for i in range(nr) :
            db.goto( i + 1 )
            nv = db.registro["NOMBRE"].strip()
            tp = db.registro["TIPO"]
            if tp == "C" :
                dt = db.registro["TEXTO"].strip()
            else :
                dt = db.registro["NUMERO"]
            self.dicc[nv]=dt
        db.cerrar()

    def fichDefecto( self ) :
        return os.path.dirname(sys.path[0]) + "\\valordef.pkl"

    def diccDefecto( self ) :
        fichDef = self.fichDefecto()
        try :
            import pickle
            pkl_file = open(fichDef, 'rb')
            diccDef = pickle.load(pkl_file)
            pkl_file.close()
        except :
            diccDef = {}
        return diccDef

    def grabaDefecto( self, diccDef ) :
        import pickle
        fichDef = self.fichDefecto()
        pkl_file = open(fichDef, 'wb')
        pickle.dump(diccDef, pkl_file)
        pkl_file.close()

    def clave( self, cClave, cRotulo=None ) :
        try :
            valor = self.dicc[cClave]
        except :
            import ED
            diccDef = self.diccDefecto()
            valorDef = diccDef[cClave] if cClave in diccDef else ""
            if cRotulo is None :
                cRotulo = cClave
            else :
                cRotulo = "Variable : [%s]\n\n%s\n"%(cClave, cRotulo)
            valor = ED.leeTexto( "Nueva clave", cRotulo, valorDef )
            if valor is None :
                sys.exit()
            diccDef[cClave] = valor
            self.grabaDefecto( diccDef )
        return valor

class clLog :
    """Facilita el manejo de un fichero de texto donde escribir"""
    def __init__( self, cFichero ) :
        self.fLog = file( cFichero, "wb" )

    def esc( self, cTexto ) :
        self.fLog.write( cTexto )

    def escF( self, cTexto, tam ) :
        self.fLog.write( cTexto.ljust(tam)[:tam] )

    def escF0( self, cTexto, tam ) :
        self.fLog.write( cTexto.rjust(tam,"0")[:tam] )

    def escNum0( self, numero, tam, decs ) :
        fmt = "%%0%dd"%tam
        try :
            self.esc( fmt % int(round(numero*10**decs)) )
        except :
            self.esc( fmt % 0 )

    def linea( self, cTexto ) :
        self.fLog.write( cTexto + "\r\n" )

    def cerrar( self ) :
        self.fLog.close()

