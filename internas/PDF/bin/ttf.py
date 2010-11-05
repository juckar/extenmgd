import struct
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reportlab.rl_config

# ###############################################################################################################
def NombreTTF( cFich ) :

    f = file( cFich, "rb" )

    x = f.read(12)

    uMajorVersion,uMinorVersion,uNumOfTables,uSearchRange,uEntrySelector,uRangeShift = struct.unpack( ">6H", x )

    cResp = ""
    siNegrita = siCursiva = 0
    for i in range( uNumOfTables ) :
        x = f.read(16)
        szTag, uCheckSum, uOffset, uLength = struct.unpack( ">4s3L", x )
        if szTag.lower() == "name" :
            f.seek( uOffset, 0 )
            x = f.read(6)
            nPos = uOffset + 6
            uFSelector, uNRCount, uStorageOffset = struct.unpack( ">3H", x )
            for i in range( uNRCount ) :
                f.seek( nPos, 0 )
                x = f.read(12)
                nPos = nPos + 12
                uPlatformID, uEncodingID, uLanguageID, uNameID, uStringLength, uStringOffset = struct.unpack( ">6H", x )
                if uNameID == 1 :
                    f.seek( uOffset + uStringOffset + uStorageOffset, 0 )
                    x = f.read( uStringLength )
                    cNombre, = struct.unpack( ">%d"%uStringLength + "s", x )
                    s = cNombre.replace( "\x00", "" )
                    if s :
                        cResp = s
                        break

    f.seek( 12, 0 )
    for i in range( uNumOfTables ) :
        x = f.read(16)
        szTag, uCheckSum, uOffset, uLength = struct.unpack( ">4s3L", x )
        if szTag.lower() == "head" :
            f.seek( uOffset+44, 0 )
            x = f.read(2)
            x, = struct.unpack( ">H", x )
            siNegrita = x & 1L
            siCursiva = ( x >> 1 ) & 1L
            break

    f.close()

    return cResp, siNegrita, siCursiva


# ###############################################################################################################
def ListaTTF( cDirFonts ) :
    import glob

    direcTTF = glob.glob( cDirFonts + "\\*.ttf" )

    diccTTF = {}

    for fichTTF in direcTTF :

        nomTTF, siNegrita, siCursiva = NombreTTF( fichTTF )

        if siNegrita and siCursiva :
            nPos = 3
        elif siCursiva :
            nPos = 2
        elif siNegrita :
            nPos = 1
        else :
            nPos = 0

        if nomTTF in diccTTF :
            lista = diccTTF[nomTTF]
            lista[nPos] = [ fichTTF, False, 0 ]
            diccTTF[nomTTF] = lista
        else :
            lista = [ ["",False, 0 ], ["",False, 0 ], ["",False, 0], ["",False, 0] ]
            lista[nPos] = [fichTTF,False,0]
            diccTTF[nomTTF] = lista

    return diccTTF

# ###############################################################################################################
def RegistraFuente( diccTTF, fuente, siNegrita, siCursiva, siSubrayado ) :

    if not fuente in diccTTF :
        if "Arial" in diccTTF :
            return RegistraFuente( diccTTF, "Arial", siNegrita, siCursiva, siSubrayado )
        else :
            return RegistraFuente( diccTTF, diccTTF.keys()[0], siNegrita, siCursiva, siSubrayado )


    lTTF = diccTTF[ fuente ]
    cNombre = fuente
    if siNegrita and siCursiva :
        nPos = 3
        cNombre += "ni"
    elif siCursiva :
        nPos = 2
        cNombre += "i"
    elif siNegrita :
        nPos = 1
        cNombre += "n"
    else :
        nPos = 0
    x = lTTF[nPos]
    if x[1] :
        return cNombre, x[2]

    cFich = x[0]
    if not cFich : # Si no tiene ningun fichero asociado, se le asigna el primero que encontremos
        for nPos in range( 4 ) :
            x = lTTF[nPos] # 0 : fichero, 1 : si dado de alta  2 : ancho,alto
            if x[0] :  # Tiene fichero ?
                siNegrita = nPos == 1 or nPos == 3
                siCursiva = nPos == 2 or nPos == 3
                return RegistraFuente( diccTTF, fuente, siNegrita, siCursiva, siSubrayado )

    # Registramos el fichero
    oTTF = TTFont(cNombre, cFich)
    pdfmetrics.registerFont(oTTF)
    lTTF[nPos][2] = (oTTF.face.ascent,oTTF.face.descent)
    lTTF[nPos][1] = True
    diccTTF[ fuente ] = lTTF
    x = lTTF[nPos]
    return cNombre, x[2]
