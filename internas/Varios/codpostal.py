# -*- coding: latin-1 -*-

import sys, os


sys.path.append( gBase + "/library.zip" )

from jFusion import *

#~ def xm( txt ) :
    #~ l = open( "hh.txt", "ab" )
    #~ l.write( txt + "\r\n" )
    #~ l.close()


# --------------------------------------------------------------------------------------------------------------------------
def lee( codigo ) :

    def Localidad( ext ) :
        try :
            cp = open( gBase + "\\Varios\\codpostales.dat"+ext, "rb" )
            txt = cp.read()
            cp.close()
            n = txt.find( codigo+"·" )
            if n >= 0 :
                return txt[n:n+80].split("·")[1]
        except :
            pass
        return ""


    localidad = Localidad( "1" )
    if not localidad :
        localidad = Localidad( "" )

    def Provincia( ext ) :
        prov = codigo[:2]
        try :
            cp = open( gBase + "\\Varios\\provincias.dat"+ext, "rb" )
            txt = cp.read()
            cp.close()
            n = txt.find( prov+"·" )
            if n >= 0 :
                return txt[n:n+80].split("·")[1]
        except :
            pass
        return ""

    provincia = Provincia( "1" )
    if not provincia :
        provincia = Provincia( "" )

    return (localidad, provincia )
# --------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------
def guarda( codigo, localidad, provincia ) :

    localidad0, provincia0 = lee( codigo )
    resp = ""
    if localidad0 != localidad :
        nuevo = "%s·%s·\n"%( codigo, localidad )
        f1 = gBase + "\\Varios\\codpostales.dat1"
        try :
            cp = open( f1, "rb" )
            txt = cp.read()
            cp.close()
            ant = "%s·%s·\n"%(codigo,localidad0)
            if ant in txt :
                txt = txt.replace( ant, nuevo )
            else :
                txt += nuevo
        except :
            txt = nuevo
        cp = open( f1, "wb" )
        cp.write( txt )
        cp.close()
        resp += localidad + "·"

    if provincia0 != provincia :
        prov = codigo[:2]
        nuevo = "%s·%s·\n"%( prov, provincia )
        f1 = gBase + "\\Varios\\provincias.dat1"
        try :
            cp = open( f1, "rb" )
            txt = cp.read()
            cp.close()
            ant = "%s·%s·\n"%( prov, provincia0 )
            if ant in txt :
                txt = txt.replace( ant, nuevo )
            else :
                txt += nuevo
        except :
            txt = nuevo
        cp = open( f1, "wb" )
        cp.write( txt )
        cp.close()
        resp += provincia + "·"

    return resp

# --------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------
def control() :

    FC = FusionMGD.clave # Forma abreviada de llamada a la función

    codigo = FC( "CODPOSTAL" )

    fichResp = FC( "FRESP" )

    siLeer = FC( "SILEER" ).strip() == "S"


    if siLeer :
        localidad, provincia = lee( codigo )
        resp = "%s·%s"% ( localidad, provincia )
    else :
        resp = guarda( codigo, FC( "LOCALIDAD" ), FC( "PROVINCIA" ) )


    f = open( fichResp, "wb" )
    f.write( resp )
    f.close()
# --------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    control()

