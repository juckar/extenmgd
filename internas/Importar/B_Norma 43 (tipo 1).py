# -*- coding: latin-1 -*-

import sys, os

sys.path.append( gBase + "/library.zip" )


from jFusion import *
from jFechas import *


############################################################################################################
def CrearTXT() :

    FC = FusionMGD.clave # Forma abreviada de llamada a la funci�n, que nos proporciona los par�metros indicados en el programa

    # Abrimos el fichero de datos
    ori = FC( "FDATOS" )
    fOri = open( ori, "rb" )


    # Creamos el fichero TXT
    TXT = FC( "DESTINO" )
    if os.path.isfile( TXT ) :
        os.remove( TXT )
    fTXT = open( TXT, "wb" )

    # Variables de comprobaci�n de la cuenta
    ctaCte = FC( "CUENTACTE" )
    nTam = len(ctaCte)
    if nTam == 20 :
        numCta = ctaCte[10:]
        numBanco = ctaCte[:4]
        siBanco = True
        siCuenta = True
    elif nTam == 10 :
        numCta = ctaCte
        siBanco = False
        siCuenta = True
    elif nTam == 4 :
        numBanco = ctaCte
        siBanco = True
        siCuenta = False
    else :
        return

    # Control de fechas, se ponen como numeros, para que sea mas facil compararlas
    nFechaInicio = cton( FC( "FECHAINICIO" ) )
    nFechaFinal = cton( FC( "FECHAFINAL" ) )

    # Variables de trabajo
    siSaltaCuenta = False # Control para grabar s�lo los que sean de la cuenta especificada
    nSaldo = 0
    siPrimero = True    # Como el concepto puede venir en dos tipos diferentes ( 22 y 23 ),
                        # no saltamos linea hasta que se registra un nuevo movimiento
                        # pero para saber que en el primero no tenemos que hacerlo usamos esta variable

    # Pasamos por todas las lineas del fichero origen
    siEnFecha = True
    for linea in fOri :

        cTipo = linea[0:2]

        if siSaltaCuenta and cTipo != "11" : # Para ir al inicio de cuenta
            continue

        elif cTipo == "11" : # Inicio de cuenta
            siSaltaCuenta = False

            banco = linea[2:6]
            if siBanco and banco != numBanco :
                siSaltaCuenta = True

            cuenta = linea[10:20]
            
            if siCuenta and cuenta != numCta :
                siSaltaCuenta = True
            
            nSaldo = int(linea[33:47]) # Se le trata como un numero entero, al imprimir desdoblaremos los decimales
            if linea[32:33] == "1" :
                nSaldo = -nSaldo


        elif cTipo == "22" : # Movimiento

            # Control de fechas
            cFecha = linea[14:16] + "/" + linea[12:14] + "/" + linea[10:12] #AAMMDD
            nFecha = cton( cFecha )
            siEnFecha = False
            
            if nFechaInicio and nFecha < nFechaInicio :
                continue # luego no se procesa
            if nFechaFinal and nFecha > nFechaFinal :
                continue # luego no se procesa

            siEnFecha = True
            nImporte = int(linea[28:42])
            cSigno = linea[27:28]
            if cSigno == "1" :
                nImporte = -nImporte

            nSaldo = nSaldo + nImporte
            cSaldo = "%d.%02d"%(nSaldo/100,abs(nSaldo)%100) # Desdoblamos para guardar

            cImporte = linea[28:40] + "." + linea[40:42]
            cImporte = cImporte.lstrip( "0" ) # Quitamos los ceros del principio
            if cSigno == "1" :
                cImporte = "-" + cImporte


            cDocumento = linea[42:52].strip() # Quitamos los caracteres sobrantes del final
            cDocumento = cDocumento.replace( "�", "." ) # Por si acaso el separador forma parte del documento

            cConcepto = linea[52:80].strip() # Quitamos los caracteres sobrantes del final
            cConcepto = cConcepto.replace( "�", "." ) # Por si acaso el separador forma parte del concepto

            # Si es el primer registro no le ponemos el salto de linea al anterior que no existe
            if siPrimero :
                siPrimero = False
            else :
                fTXT.write( "\r\n" ) # Fin de linea = retorno de carro+salto de linea

            fTXT.write( cFecha + "�" + cImporte + "�" + cDocumento + "�" + cSaldo + "�" + cConcepto  )

        elif cTipo == "23" and siEnFecha : # Concepto adicional
            cConcepto = linea[4:80].strip()
            cConcepto = cConcepto.lstrip()
            cConcepto = cConcepto.replace( "�", "." )
            fTXT.write( " " + cConcepto )

        # El resto de tipos no nos sirven de nada


    #Cerramos
    fOri.close()
    fTXT.close()



if __name__ == '__main__':
    try :
        CrearTXT()
    except :
        sys.exit(0)

"""
Identificador de registro 1 2 2 Num�rico
Clave de Banco 3 6 4 Num�rico
Clave de Oficina 7 10 4 Num�rico
N� de Cuenta 11 20 10 Num�rico
Fecha inicial 21 26 6 Num�rico
Fecha Final 27 32 6 Num�rico
Clave Debe o Haber 33 33 1 Num�rico
Importe saldo inicial 34 47 14 Num�rico
Clave de divisa 48 50 3 Num�rico
Modalidad de informaci�n 51 51 1 Num�rico
Nombre abreviado 52 77 26 Alfanum�rico
Libre 78 80 3 Relleno a blancos

REGISTRO PRINCIPAL DE MOVIMIENTOS
Identificador de registro 1 2 2 Num�rico
Libre 3 6 4 Relleno a blancos
Clave de Oficina de origen 7 10 4 Num�rico
Fecha Operaci�n 11 16 6 Num�rico
Fecha Valor 17 22 6 Num�rico
Concepto com�n 23 24 2 Num�rico
Concepto propio 25 27 3 Num�rico
Clave Debe o Haber 28 28 1 Num�rico
Importe 29 42 14 Num�rico
N� de documento 43 52 10 Num�rico
Referencia 1 53 64 12 Num�rico
Referencia 2 65 80 16 Alfanum�rico

REGISTROS COMPLEMENTARIOS DE CONCEPTO
Identificador de registro 1 2 2 Num�rico
C�digo de dato 3 4 2 Num�rico
Conceptos 1� - 3� - 5� -7� y 9� 5 42 38 Alfanum�rico
Conceptos 2� - 4� - 6� - 8� y 10� 43 80 38 Alfanum�rico

REGISTRO FINAL DE CUENTA
Identificador de registro 1 2 2 Num�rico
Clave de Banco 3 6 4 Num�rico
Clave de Oficina 7 10 4 Num�rico
N� de Cuenta 11 20 10 Num�rico
N� Apuntes Debe 21 25 5 Num�rico
Total Importes Debe 26 39 14 Num�rico
N� Apuntes Haber 40 44 5 Num�rico
Total Importes Haber 45 58 14 Num�rico
C�digo Saldo Final 59 59 1 Num�rico
Saldo Final 60 73 14 Num�rico
Clave de Divisa 74 76 3 Num�rico
Libre 77 80 4 Relleno a blancos
"""
