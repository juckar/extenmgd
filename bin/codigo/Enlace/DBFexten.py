# -*- coding: latin-1 -*-

from Enlace import *

#===================================================================================================================
class DBFexten :

    def __init__( self, numero ) :
        
        dll = enlaceMGD() 
        
        self.numDBF = numero
        self.cierraDBF = dll.cierraDBF
        self.ordenDBF = dll.ordenDBF
        self.ordenDBF_1 = dll.ordenDBF_1
        self.ordenDBF_1R = dll.ordenDBF_1R
        self.ordenDBF_2 = dll.ordenDBF_2
        self.ordenDBF_R = dll.ordenDBF_R
        self.accessDBF = dll.accessDBF
        self.marcaDBF = dll.marcaDBF
        self.recuperaDBF = dll.recuperaDBF
        self.contabilizaDBF = dll.contabilizaDBF
        self.ultimoDBF = dll.ultimoDBF
        self.cnumeroDBF = dll.cnumeroDBF
        
        self.liFields = []
        self.nomFields = {}

    def cierra( self ) :
        self.cierraDBF( self.numDBF )

    def orden_0( self, arg ) :
        self.ordenDBF( self.numDBF, arg )

    def orden_1( self, arg, arg1 ) :
        self.ordenDBF_1( self.numDBF, arg, convierteZ(arg1) )

    def orden_2( self, arg, arg1, arg2 ) :
        self.ordenDBF_2( self.numDBF, arg, convierteZ(arg1), convierteZ(arg2) )

    def orden_1R( self, arg, arg1 ) :
        return Zconvierte( self.ordenDBF_1R( self.numDBF, arg, convierteZ(arg1) ) )

    def access( self, arg ) :
        return Zconvierte( self.accessDBF( self.numDBF, arg ) )

    def close( self ) :
        self.orden_0( "CLOSE" )

    def reccount( self ) :
        return self.access( "RECCOUNT" )

    def recno( self ) :
        return self.access( "RECNO" )

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
        self.marcaDBF( self.numDBF )

    def recupera( self ) :
        self.recuperaDBF( self.numDBF )

    def contabiliza( self ) :
        self.contabilizaDBF( self.numDBF )

    def ultimo( self ) :
        return self.ultimoDBF( self.numDBF )

    def tipo_cnumero( self, fecha, importe=0, banco=0 ) :
        resp = Zconvierte( self.cnumeroDBF( self.numDBF, convierteZ(fecha), convierteZ(importe), convierteZ( banco ) ) )
        return resp[0], int(resp[1:])

    def listaCampos( self ) :
        if len(self.liFields) == 0 :
            cad = self.access( "FINFO" )
            liF = cad.split( "·" )
            for nc, uno in enumerate(liF) :
                li = uno.split( "|" )
                nom = li[0]
                self.liFields.append( Field( nom, li[1], int(li[2]), int(li[3]) ) )
                self.nomFields[nom] = nc
                
        return self.liFields
        
    def __getattr__( self, nombre ) :
        if nombre.isupper() :
            if len(self.liFields) == 0 :
                self.listaCampos()
        
            if nombre in self.nomFields :
                return self.fieldget( nombre )
            else :
                c = ",".join(self.nomFields.keys())
                raise exceptions.NameError( self._nombre + " : campo desconocido=" + nombre + " " + c)
                return None
        else :
            return self.__dict__[nombre]

    def __setattr__( self, nombre, valor ) :
        if nombre.isupper() :
            if len(self.liFields) == 0 :
                self.listaCampos()
            
            if nombre in self.nomFields :
                self.fieldput( nombre, valor )
                return
            else :
                c = ",".join(self.nomFields.keys())
                raise exceptions.NameError( self._nombre + " : campo desconocido=" + nombre + " " + c)
        else :
            self.__dict__[nombre] = valor

