#-*- coding: latin-1 -*-

import datetime

class clFecha :

    def __init__( self, xdia=0, xmes=0, xeje=0 ) :
        self.dia = xdia
        self.mes = xmes
        self.eje = xeje
        if xmes > 0 and  xeje < 1000 :
            self.eje = xeje + 2000


    def __str__(self) :
        return "%02d/%02d/%04d" % ( self.dia, self.mes, self.eje )

    def fecha2DB(self) :
        "Convierte la fecha a formato año-mes-dia, lo que permite ordenaciones correctas"
        return "%04d%02d%02d" % ( self.eje, self.mes, self.dia )

    def DB2fecha( self, sfecha ) :
        "Lee una fecha en formato año-mes-dia"
        sfecha = sfecha.strip( )
        if sfecha == "" :
            self.dia = 0
            self.mes = 0
            self.eje = 0
        else :
            self.dia = int(sfecha[6:])
            self.mes = int(sfecha[4:6])
            self.eje = int(sfecha[:4])

    def __sub__(self, otra ) :
        d = datetime.date( self.eje, self.mes, self.dia )
        if isinstance(otra, int ) :
            d = d.fromordinal( d.toordinal() - otra )
            return clFecha( d.day, d.month, d.year )
        elif isinstance( otra, clFecha ) :
            d1 = datetime.date( otra.eje, otra.mes, otra.dia )
            return d.toordinal() - d1.toordinal()
        return self

    def __add__(self, otra ) :
        if isinstance(otra, int ) :
            return self.__sub__( -otra )
        return self

    def datetime( self ) :
        return datetime.date( self.eje, self.mes, self.dia )

    def ordinal( self ) :
        if self.eje == 0 :
            return 0
        d = datetime.date( self.eje, self.mes, self.dia )
        return d.toordinal()



def ctod( cfecha ) :
    l = cfecha.split("/")
    if len(l) != 3 :
        l = cfecha.split("-")
        if len(l) != 3 :
            return clFecha( 0, 0, 0 )
    return clFecha( int(l[0]), int(l[1]), int(l[2]) )

def cton( cfecha ) :
    f = ctod( cfecha )
    return f.ordinal()


def DB2fecha( sFecha ) :
    d = clFecha()
    d.DB2fecha( sFecha )
    return d

