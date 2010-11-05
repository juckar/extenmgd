# -*- coding: latin-1 -*-

import sys, os

sys.path.append( gBase + "/library.zip" )


from jFusion import *
from jFechas import *


############################################################################################################
def CrearTXT() :

    FC = FusionMGD.clave # Forma abreviada de llamada a la función, que nos proporciona los parámetros indicados en el programa

    # Abrimos el fichero de datos
    ori = FC( "FDATOS" )
    fOri = open( ori, "rb" )


    # Creamos el fichero TXT
    TXT = FC( "DESTINO" )
    if os.path.isfile( TXT ) :
        os.remove( TXT )
    fTXT = open( TXT, "wb" )

    # Variables de comprobación de la cuenta
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
    siSaltaCuenta = False # Control para grabar sólo los que sean de la cuenta especificada
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
            cDocumento = cDocumento.replace( "·", "." ) # Por si acaso el separador forma parte del documento

            cConcepto = linea[52:80].strip() # Quitamos los caracteres sobrantes del final
            cConcepto = cConcepto.replace( "·", "." ) # Por si acaso el separador forma parte del concepto

            # Si es el primer registro no le ponemos el salto de linea al anterior que no existe
            if siPrimero :
                siPrimero = False
            else :
                fTXT.write( "\r\n" ) # Fin de linea = retorno de carro+salto de linea

            fTXT.write( cFecha + "·" + cImporte + "·" + cDocumento + "·" + cSaldo + "·" + cConcepto  )

        elif cTipo == "23" and siEnFecha : # Concepto adicional
            cConcepto = linea[4:80].strip()
            cConcepto = cConcepto.lstrip()
            cConcepto = cConcepto.replace( "·", "." )
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
Identificador de registro 1 2 2 Numérico
Clave de Banco 3 6 4 Numérico
Clave de Oficina 7 10 4 Numérico
Nº de Cuenta 11 20 10 Numérico
Fecha inicial 21 26 6 Numérico
Fecha Final 27 32 6 Numérico
Clave Debe o Haber 33 33 1 Numérico
Importe saldo inicial 34 47 14 Numérico
Clave de divisa 48 50 3 Numérico
Modalidad de información 51 51 1 Numérico
Nombre abreviado 52 77 26 Alfanumérico
Libre 78 80 3 Relleno a blancos

REGISTRO PRINCIPAL DE MOVIMIENTOS
Identificador de registro 1 2 2 Numérico
Libre 3 6 4 Relleno a blancos
Clave de Oficina de origen 7 10 4 Numérico
Fecha Operación 11 16 6 Numérico
Fecha Valor 17 22 6 Numérico
Concepto común 23 24 2 Numérico
Concepto propio 25 27 3 Numérico
Clave Debe o Haber 28 28 1 Numérico
Importe 29 42 14 Numérico
Nº de documento 43 52 10 Numérico
Referencia 1 53 64 12 Numérico
Referencia 2 65 80 16 Alfanumérico

REGISTROS COMPLEMENTARIOS DE CONCEPTO
Identificador de registro 1 2 2 Numérico
Código de dato 3 4 2 Numérico
Conceptos 1º - 3º - 5º -7º y 9º 5 42 38 Alfanumérico
Conceptos 2º - 4º - 6º - 8º y 10º 43 80 38 Alfanumérico

REGISTRO FINAL DE CUENTA
Identificador de registro 1 2 2 Numérico
Clave de Banco 3 6 4 Numérico
Clave de Oficina 7 10 4 Numérico
Nº de Cuenta 11 20 10 Numérico
Nº Apuntes Debe 21 25 5 Numérico
Total Importes Debe 26 39 14 Numérico
Nº Apuntes Haber 40 44 5 Numérico
Total Importes Haber 45 58 14 Numérico
Código Saldo Final 59 59 1 Numérico
Saldo Final 60 73 14 Numérico
Clave de Divisa 74 76 3 Numérico
Libre 77 80 4 Relleno a blancos
"""
