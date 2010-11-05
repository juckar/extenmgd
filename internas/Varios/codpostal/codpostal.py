# -*- coding: latin-1 -*-

import sys, os


sys.path.append( gBase + "/library.zip" )

from jFusion import *


# --------------------------------------------------------------------------------------------------------------------------
def control() :

    FC = FusionMGD.clave # Forma abreviada de llamada a la función

    codigo = FC( "CODPOSTAL" )

    fichResp = FC( "FRESP" )

    f = open( fichResp, "wb" )
    f.write( resp )
    f.close()
# --------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    control()

