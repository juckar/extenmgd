# -*- coding: latin-1 -*-

import sys, os


sys.path.append( gBase + "/library.zip" )

from jFusion import *


# --------------------------------------------------------------------------------------------------------------------------
def controlCIF( cCIF ) :

    # 9 dígitos
    if len(cCIF) != 9 :
        return "ha de contener nueve dígitos"

    # El primero una letra
    cTipo = cCIF[0]
    cTipos = "ABCDEFGHJPQRSUVNW"
    if cTipo not in cTipos :
        return "el primer carácter ha de ser uno de los siguientes : " + cTipos

    # Los 8 siguientes han de se números
    cNum = cCIF[1:9]
    if not cNum.isdigit() :
        return "los caracteres en posiciones 1 a 9, han de ser números"

    # El último es el dígito de control
    # Se toman únicamente los números centrales (en python se empieza desde 0)
    #   1. Sumar los dígitos de la posiciones pares.
    nPar = int(cCIF[2])+int(cCIF[4])+int(cCIF[6])
    #   2. Para cada uno de los dígitos de la posiciones impares, multiplicarlo por 2 y sumar los dígitos del resultado.
    nImpar = 0
    for pos in [ 1, 3, 5, 7 ] :
        n = int(cCIF[pos])*2
        nImpar += int(n/10) + n%10
    #   3. Calcular la suma
    nTotal = nPar + nImpar
    #   4. Tomar sólo el dígito de las unidades de C y restárselo a 10. Esta resta nos da D.
    nDigito = (10 - nTotal%10)%10
    cDigito = cCIF[8]
    if cTipo in "CKLMNPQRSVW" :
        dcLetras = "JABCDEFGHI"
        cLetra = dcLetras[nDigito]
        if cDigito != cLetra :
            return "no es correcto el dígito de control ha de ser %s"%cLetra
    else :
        if cDigito != str(nDigito) :
            return "no es correcto el dígito de control ha de ser %s"%str(nDigito)

    return None
# --------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------
def letraNIF( cNIFsinLetra ) :
    nNIF = int(cNIFsinLetra)
    cLetras = "TRWAGMYFPDXBNJZSQVHLCKE"
    return cLetras[nNIF%23]
# --------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------
def controlCIF_NIF( cCIF_NIF ) :
    tamCIF_NIF = len(cCIF_NIF)
    if tamCIF_NIF < 5 :
        return "Error NIF : formato erróneo."

    cPrimero = cCIF_NIF[0]
    if cPrimero in "0123456789XYZ" :
        if cPrimero in "XYZ" : # Extranjeros
            digito = "0" if cPrimero == "X" else ( "1" if cPrimero == "Y" else "2" )
            cCIF_NIF = digito + cCIF_NIF[1:]
        cLetra = "-"
        if cCIF_NIF[-1].isalpha() :
            cLetra = cCIF_NIF[-1]
            cCIF_NIF = cCIF_NIF[:-1]
        if not cCIF_NIF.isdigit() :
            return "Error : NIF erróneo."
        cLetraDebe = letraNIF(  cCIF_NIF )
        if cLetraDebe != cLetra :
            return "Error NIF : la letra del NIF tiene que ser %s."%cLetraDebe

        return None

    else :
        error = controlCIF( cCIF_NIF )
        if error :
            error = "Error CIF : %s."%error
        return error
# --------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------
def controlDCbanco( c20 ) :

    c20 = c20.strip()
    if not c20 :
        return None

    cError = None
    if len(c20) != 20 :
        cError = "no tiene 20 dígitos"
    elif not c20.isdigit() :
        cError = "sólo puede contener números"
    else :
        liNum = [ int(x) for x in c20 ]

        liH1 = [ 4, 8, 5, 10, 9, 7, 3, 6 ]
        H1 = 0
        for numero, peso in enumerate(liH1) :
            H1 += peso*liNum[numero]

        liI1 = [ 1, 2, 4, 8, 5, 10, 9, 7, 3, 6 ]
        I1 = 0
        for numero, peso in enumerate(liI1) :
            I1 += peso*liNum[numero+10]

        ph = H1%11
        if ph == 0 :
            dc = 0
        elif ph == 1 :
            dc = 10
        else :
            dc = 10*(11-ph)

        pi = I1%11
        if pi == 0 :
            dc += 0
        elif pi == 1 :
            dc += 1
        else :
            dc += 11-pi

        num = liNum[8]*10 + liNum[9]
        if num != dc :
            cError = "el dígito de control ha de ser %02d (y tiene %02d)"%( dc, num )

    if cError :
        return "Error en los datos bancarios (20 dígitos) : %s." % cError

    return cError

# --------------------------------------------------------------------------------------------------------------------------
def control() :

    FC = FusionMGD.clave # Forma abreviada de llamada a la función

    error = controlCIF_NIF( FC( "NIF" ) )

    errorDC = controlDCbanco( FC( "20DIGITOS" ) )

    fichResp = FC( "FRESP" )

    f = open( fichResp, "wb" )
    if error :
        f.write( error )
    if errorDC :
        if error :
            f.write( "\r\n" )
        f.write( errorDC )
    f.close()
# --------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    control()

