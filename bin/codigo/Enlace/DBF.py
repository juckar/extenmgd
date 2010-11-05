# -*- coding: latin-1 -*-

import exceptions
import datetime
import types

from Enlace import *


class DBF :

    def __init__( self, nombre, siShare = False, open = True ) :
        
        self._nombre = nombre
        self.siShare = siShare
        self.liFields = []
        self.nomFields = {}

        dll = enlaceDBF() 
            
        self.dbf_open = dll.dbf_open
            
        self.dbf_orden = dll.dbf_orden
        self.dbf_orden_1 = dll.dbf_orden_1
        self.dbf_orden_1R = dll.dbf_orden_1R
        self.dbf_orden_2 = dll.dbf_orden_2
        self.dbf_orden_R = dll.dbf_orden_R
            
        self.dbf_access = dll.dbf_access
            
        self.dbf_marca = dll.dbf_marca
        self.dbf_recupera = dll.dbf_recupera
            
        self.dbf_close = dll.dbf_close

        self.dbf_field = dll.dbf_field

        self.dbf_new = dll.dbf_new
        self.dbf_newCampo = dll.dbf_newCampo
        self.dbf_newCrea = dll.dbf_newCrea
        
        if open :
            self.open()
        

    def open( self ) :
        self.numDBF = self.dbf_open( self._nombre, 1 if self.siShare else 0 )

    def orden_0( self, arg ) :
        self.dbf_orden( self.numDBF, arg )

    def orden_0R( self, arg ) :
        return Zconvierte(self.dbf_orden( self.numDBF, arg ))

    def orden_1( self, arg, arg1 ) :
        self.dbf_orden_1( self.numDBF, arg, convierteZ(arg1) )

    def orden_2( self, arg, arg1, arg2 ) :
        self.dbf_orden_2( self.numDBF, arg, convierteZ(arg1), convierteZ(arg2) )

    def orden_1R( self, arg, arg1 ) :
        return Zconvierte( self.dbf_orden_1R( self.numDBF, arg, convierteZ(arg1) ) )

    def access( self, arg ) :
        return Zconvierte( self.dbf_access( self.numDBF, arg ) )

    def close( self ) :
        self.dbf_close( self.numDBF )

    def reccount( self ) :
        return self.access( "RECCOUNT" )

    def recno( self ) :
        return self.access( "RECNO" )

    def fcount( self ) :
        return self.access( "FCOUNT" )

    def goto( self, registro ) :
        self.orden_1( "GOTO", registro )

    def skip( self, numero = 1 ) :
        self.orden_1( "SKIP", numero )

    def gotop( self ) :
        self.orden_0( "GOTOP" )

    def gobottom( self ) :
        self.orden_0( "GOBOTTOM" )

    def eof( self ) :
        return self.access( "EOF" )

    def bof( self ) :
        return self.access( "BOF" )

    def setfilter( self, filtro ) :
        self.orden_1( "SETFILTER", filtro )

    def setorder( self, indice ) :
        self.orden_1( "SETORDER", indice )

    def reindex( self ) :
        self.orden_0( "REINDEX" )

    def fieldget( self, campo ) :
        return self.orden_1R( "FIELDGET", campo )

    def fieldput( self, campo, valor ) :
        self.orden_2( "FIELDPUT", campo, valor )

    def commit( self ) :
        self.orden_0( "COMMIT" )

    def zap( self ) :
        self.orden_0( "ZAP" )

    def pack( self ) :
        self.orden_0( "PACK" )

    def delete( self ) :
        self.orden_0( "DELETE" )

    def deleted( self ) :
        return orden_R( "DELETED" )

    def seek( self, busqueda ) :
        return self.orden_1R( "SEEK", busqueda )

    def locate( self, condicion ) :
        return self.orden_1R( "LOCATE", condicion )

    def locatecontinue( self ) :
        return self.orden_R( "CONTINUE" )

    def append( self ) :
        self.orden_0( "APPEND" )

    def marca( self ) :
        self.dbf_marca( self.numDBF )

    def recupera( self ) :
        self.dbf_recupera( self.numDBF )
        
    def newField( self, nombre, tipo, ancho = 0, decimales = 0 ) :
        self.liFields.append( Field( nombre, tipo, ancho, decimales ) )
    
    def create( self ) :
        self.numDBF = self.dbf_new( self._nombre ) 
        for f in self.liFields :
            self.dbf_newCampo( self.numDBF, f.nombre, f.tipo, f.ancho, f.decimales )
        self.numDBF = self.dbf_newCrea( self.numDBF )
        
    def siError( self ) :
        return self.numDBF == -1
        
    def listaCampos( self ) :
        if len(self.liFields) == 0 :
            numCampos = self.fcount()
            nc = 0
            for x in range( 1, numCampos+1 ) :
                c = self.dbf_field( self.numDBF, x )
                li = c.split( "|" )
                self.liFields.append( Field( li[0], li[1], int(li[2]), int(li[3]) ) )
                self.nomFields[li[0]] = nc
                nc += 1
                
        return self.liFields
        
    def __getattr__( self, nombre ) :
        if len(self.liFields) == 0 :
            self.listaCampos()
        
        if nombre in self.nomFields :
            return self.fieldget( nombre )
        elif nombre.isupper() :
            c = ",".join(self.nomFields.keys())
            raise exceptions.NameError( self._nombre + " : campo desconocido=" + nombre + " " + c)
            return None
        else :
            return self.__dict__[nombre]

    def __setattr__( self, nombre, valor ) :
        if nombre.isupper() :
            if len(self.liFields) == 0 :
                self.listaCampos()
            
            if nom in self.nomFields :
                self.fieldput( nom, valor )
                return
            c = ",".join(self.nomFields.keys())
            raise exceptions.NameError( self._nombre + " : campo desconocido=" + nombre + " " + c)
        else :
            self.__dict__[nombre] = valor

#-----------------------------------------------------------------------------------------------------------------------------------------
#~ prueba.py

import os

ponDirEnlace( "c:/mgd/bin" )

dcomun = "c:/mgd/comun"
nomDBF = os.path.abspath(os.path.join( dcomun, "empresas.dbf" ))

dbEmp = DBF( nomDBF )

if not dbEmp.siError() :
    dbEmp.gotop()
    while not dbEmp.eof() :
        print dbEmp.NUMERO, dbEmp.NOMBRE
        dbEmp.skip(1)
        
    dbEmp.close()
else :
    print dbEmp.numDBF


