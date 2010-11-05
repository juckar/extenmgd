# -*- coding: latin-1 -*-
#================================================================================================================================================
# Autor Jesús Martínez
# Licencia GPL v. 3
#================================================================================================================================================

import sys
reload(sys)
sys.setdefaultencoding("latin-1")

import Util.Config as Config
import Enlace.Enlace as Enlace

tipo = sys.argv[1] 

# "x":externas
if tipo.lower() == "x" :

    ferr = open("error.log", "at")
    sys.stderr = ferr

    modulo = sys.argv[2]
    empresa = sys.argv[3]

    config = Config.ConfigX( tipo, modulo, empresa )

    if len(sys.argv) > 4 :
        config.arg = sys.argv[4]

    Enlace.ponDirEnlace( config.dirBIN )


    sys.path.append( config.dirModulo )
    import Inicio
    # Existe un fichero en carpeta = Inicio que tiene una función inicio, a la que se le pasa toda la información de la localización de las carpetas
    Inicio.inicio(config)
    
    ferr.close()
    
# resto:internas
else :
    from jFusion import clFusion

    config = Config.ConfigI( )
    Enlace.ponDirEnlace( config.dirBIN )
    
    gBase = config.dirBINX

    ordenDBF = sys.argv[1]
    FusionMGD = clFusion( ordenDBF )
    
    execfile( FusionMGD.clave( "ORIGEN" ),locals())



