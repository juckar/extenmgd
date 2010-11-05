# -*- coding: latin-1 -*-
"""
Rutinas generales de apoyo.
"""
import os

#================================================================================================================================================
def tamFichero( fichero ) :
    return os.path.getsize( fichero ) if os.path.isfile( fichero ) else -1

#================================================================================================================================================
def ini2dic( fichero ) :

    dic = {}

    if os.path.isfile( fichero) :

        f = open( fichero, "rb" )

        for linea in f :
            linea = linea.strip()
            if linea :
                if linea.startswith( "[" ) :
                    clave = linea[1:-1]
                    dic[clave] = {}
                else :
                    n = linea.find( "=" )
                    if n :
                        clave1 = linea[:n].strip()
                        valor = linea[n+1:].strip()
                        dic[clave][clave1] = valor
        f.close()

    return dic
#================================================================================================================================================
def dic2ini( fichero, dic ) :
    f = open( fichero, "wb" )
    for k in dic.keys() :
        f.write( "[%s]\n"%k )
        dic1 = dic[k]
        for k1 in dic1.keys() :
            f.write( "%s=%s\r\n"%(k1,dic1[k1]) )
    f.close()
#================================================================================================================================================
#================================================================================================================================================
def ini2dicSimple( fichero ) :
    """
    lista de variable=valor
    """

    dic = {}

    if os.path.isfile( fichero) :
        
        f = open( fichero, "rb" )

        for linea in f :
            linea = linea.strip()
            if linea :
                n = linea.find( "=" )
                if n :
                    clave = linea[:n].strip()
                    valor = linea[n+1:].strip()
                    dic[clave] = valor
        f.close()

    return dic
#================================================================================================================================================
def dic2iniSimple( fichero, dic ) :
    f = open( fichero, "wb" )
    for k,v in dic.iteritems() :
        f.write( "%s=%s\r\n"%(k,v) )
    f.close()
#================================================================================================================================================
def memowrit( fichero, txt ) :
    f = open( fichero, "wb" )
    f.write( txt )
    f.close()
