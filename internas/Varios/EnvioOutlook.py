# -*- coding: latin-1 -*-

import sys, os

sys.path.append( gBase + "/library.zip" )

from jFusion import *

# --------------------------------------------------------------------------------------------------------------------------
def envio() :

    FC = FusionMGD.clave # Forma abreviada de llamada a la función

    clll = open( gBase + "\\Varios\\config.lll", "wb" )

    clll.write( "de=%s\r\n" %"NoImplementado@no.com" )
    clll.write( "para=%s\r\n" % FC( "DESTINO" ) )
    clll.write( "asunto=%s\r\n" % FC( "ASUNTO" ) )
    mensaje = FC( "MENSAJE" )
    if "\r\n" in mensaje :
        mensaje = mensaje.replace( "\r\n", "|" )
    if "\r" in mensaje :
        mensaje = mensaje.replace( "\r", "|" )
    if "\n" in mensaje :
        mensaje = mensaje.replace( "\n", "|" )

    clll.write( "cuerpo=%s\r\n" % mensaje )
    clll.write( "archivo=%s\r\n" % FC( "FICHPDF" ) )
    clll.close()

    os.startfile( gBase + "\\Varios\\EnvioMail.exe" )
# --------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    envio()

