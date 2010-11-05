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

    dicConceptoIBERCAJA = { "071":"AMERICAN EXPRESS",
                            "025":"ASOCIACION BENEFICA",
                            "059":"CAJERO OTRA ENTIDAD",
                            "072":"CHEQUE CARBURANTE",
                            "057":"COMISIONES Y GASTOS",
                            "055":"CORRECCION APUNTE",
                            "053":"DISPOS. EFECTIVO TAR",
                            "036":"DOCUMENTOS AL COBRO",
                            "041":"EFECTO CORTE INGLES",
                            "064":"EFECTO RECLAMADO",
                            "048":"FONDOS DE INVERSION",
                            "088":"GASOLEO BONIFICADO",
                            "006":"IMPUESTO LOCAL",
                            "046":"INTERESES-COMIS.CRED",
                            "056":"MANTENIMIENTO DE CUE",
                            "045":"OBRA SOCIAL IBERCAJA",
                            "037":"OPERACION S.E.M.P.A.",
                            "089":"PASO A ACTIVOS EN SU",
                            "020":"PREMIO IBERCAJA",
                            "079":"PRODUCTO AGRICOLA",
                            "007":"RECIBO ALQUILER",
                            "002":"RECIBO ELECTRICIDAD",
                            "067":"RECIBO VARIOS",
                            "054":"REINTEGRO OTRA ENTID",
                            "028":"SERVICIOS-SUMINISTRO",
                            "052":"TARJETA IBERCAJA",
                            "013":"TRANSFERENCIA INTERN",
                            "030":"VARIOS",
                            "080":"ANTICIPO",
                            "043":"BECAS",
                            "022":"CENTRO DE ENSEÑANZA",
                            "023":"COLEGIO PROFESIONAL",
                            "069":"COMPRA DE ENTRADAS",
                            "032":"CUSTODIA DEPOSITOS",
                            "016":"DIVIDENDOS Y CUPONES",
                            "009":"EFECTO COMERCIAL",
                            "026":"EFECTO EDITORIAL",
                            "029":"EFECTOS ENSERES HOGA",
                            "068":"FONDOS DE PENSIONES",
                            "065":"GASTOS REMESA EFECTO",
                            "073":"INGRESO PROMOCION DE",
                            "040":"LIQUIDACION INTERESE",
                            "018":"MONEDA EXTRANJERA",
                            "021":"OPERACION CON CHEQUE",
                            "012":"OPERACION VALORES",
                            "019":"PENSION",
                            "082":"PRESTACION SOCIAL",
                            "074":"PRODUCTO GANADERO",
                            "005":"RECIBO CONTRIBUCION",
                            "003":"RECIBO GAS",
                            "081":"REFUNDICION APUNTES",
                            "034":"RETROCESION APUNTE",
                            "035":"SUBSIDIO DE DESEMPLE",
                            "070":"TARJETA VISA",
                            "038":"TRASPASO AUTOMATICO",
                            "085":"VENCIMIENTO INVERSIO",
                            "024":"ASOC. CULTURAL-RECRE",
                            "051":"CAJERO AUTOMATICO",
                            "075":"CEREALES Y GIRASOL",
                            "080":"COMISION DESCUBIERTO",
                            "031":"COMUNIDAD PROPIETARI",
                            "062":"DESCUENTO EFECTOS",
                            "010":"DOCUMENTO DEVUELTO",
                            "027":"EFECTO CONSTRUCTORA",
                            "063":"EFECTO IMPAGADO",
                            "050":"FACTURA A CARGO IBER",
                            "076":"FRUTAS Y HORTALIZAS",
                            "008":"IMPUESTO ESTATAL",
                            "015":"INTERESES",
                            "078":"MAIZ Y VINO",
                            "017":"NOMINA",
                            "000":"OPERACION EN EFECTIV",
                            "083":"PAGO PROVEEDORES",
                            "049":"PLAN DE AHORRO",
                            "011":"PRESTAMO-CREDITO-AVA",
                            "001":"RECIBO AGUA",
                            "044":"RECIBO DE SEGUROS",
                            "004":"RECIBO TELEFONO",
                            "047":"REGULACION SALDO CRE",
                            "033":"SEGURIDAD SOCIAL",
                            "077":"SUBVENCION AGROPECUA",
                            "014":"TRANSFERENCIA EXTERN",
                            "058":"TRASPASO POR CANCELA" }

    # Control de fechas, se ponen como numeros, para que sea mas facil compararlas
    nFechaInicio = cton( FC( "FECHAINICIO" ) )
    nFechaFinal = cton( FC( "FECHAFINAL" ) )

    # Variables de trabajo
    siSaltaCuenta = False # Control para grabar sólo los que sean de la cuenta especificada
    nSaldo = 0
    siPrimero = True    # Como el concepto puede venir en dos tipos diferentes ( 22 y 23 ),
                        # no saltamos linea hasta que se registra un nuevo movimiento
                        # pero para saber que en el primero no tenemos que hacerlo usamos esta variable
    cReferencia = "" # Para guardar referencia del tipo 22

    # Pasamos por todas las lineas del fichero origen
    siEnFecha = False
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

            cReferencia = linea[64:80].strip()

            # Si es el primer registro no le ponemos el salto de linea al anterior que no existe
            if siPrimero :
                siPrimero = False
            else :
                fTXT.write( "\r\n" ) # Fin de linea = retorno de carro+salto de linea

            #Concepto propio 25 27 3 Numérico
            clave = linea[24:27]
            if clave in dicConceptoIBERCAJA :
                cConceptoPropio = dicConceptoIBERCAJA[clave] + " "
            else :
                cConceptoPropio = ""

            fTXT.write( cFecha + "·" + cImporte + "·" + cDocumento + "·" + cSaldo + "·" + cConceptoPropio + cDocumento + " "  )

        elif cTipo == "23" and siEnFecha : # Concepto adicional
            cConcepto = linea[42:80].lstrip()
            c = linea[4:42].strip()
            if len(c) > 0 :
                cConcepto = cConcepto.strip() + " - " + c
            if len(cReferencia) > 0 :
                #~ cConcepto = cConcepto.strip() + " ( " + cReferencia + " )"
                cReferencia = "" # por si acaso
            while "  " in cConcepto :
                cConcepto = cConcepto.replace( "  ", " " )
            cConcepto = cConcepto.replace( "·", "." )
            fTXT.write( cConcepto + " " )

        # El resto de tipos no nos sirven de nada


    #Cerramos
    fOri.close()
    fTXT.close()



if __name__ == '__main__':
    try :
        CrearTXT()
    except :
        sys.exit(0)

