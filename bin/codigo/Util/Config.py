# -*- coding: latin-1 -*-
#================================================================================================================================================
# Autor Jesús Martínez
# Licencia GPL v. 3
#================================================================================================================================================
import os
import sys

def absjoin( dir1, dir2 ) :
    return os.path.abspath(os.path.join(dir1, dir2))

class ConfigX :
    def __init__( self, tipo, carpeta, empresa ) :

        self.empresa = int(empresa)

        # Carpetas
        # mgd/bin/exten/bin mgd/bin/exten/externas
        self.dirBINX = os.path.abspath(os.path.realpath(os.path.dirname(sys.argv[0])))
        self.dirEXTEN = absjoin( self.dirBINX, ".." )
        self.dirBIN = absjoin( self.dirEXTEN, ".." )
        self.dirMGD = absjoin( self.dirBIN, ".." )
        self.dirModulo = absjoin( self.dirEXTEN, "externas" + "/" + carpeta )
        self.dirEmpresa = absjoin( self.dirMGD, "MGD%03d"%self.empresa )
        self.dirComun = absjoin( self.dirMGD, "Comun" )
        self.dirTMP = absjoin( self.dirMGD, "TMP" )
        

class ConfigI :
    def __init__( self ) :

        # Carpetas
        # mgd/bin/exten/bin mgd/bin/exten/externas
        self.dirBINX = os.path.abspath(os.path.realpath(os.path.dirname(sys.argv[0])))
        self.dirEXTEN = absjoin( self.dirBINX, ".." )
        self.dirBIN = absjoin( self.dirEXTEN, ".." )
        self.dirMGD = absjoin( self.dirBIN, ".." )
        self.dirINTERNAS = absjoin( self.dirEXTEN, "internas" )
        self.dirComun = absjoin( self.dirMGD, "Comun" )
        self.dirTMP = absjoin( self.dirMGD, "TMP" )
        
        
    
