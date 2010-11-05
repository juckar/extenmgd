# -*- coding: latin-1 -*-
#================================================================================================================================================

import Varios


#================================================================================================================================================
def emitida( siSoloErrores, empresa, reg ) :
    
    
    error = ""

    # rmas = lista de registros adicionales
    rmas = reg["MAS"] if "MAS" in reg else []
    
    # Conversiones usuales
    def xcuenta( txt ) :
        return Varios.cuenta( txt, empresa.tamcuenta )
    xfecha = Varios.c2date
    def xfloat( txt ) :
        return float(txt)/100.00 if txt else 0.00
    def xporc( txt ) :
        return float(txt) if txt else 0.00
    
    
    # fecha ---------------------------------------------------------------------------------------
    #   06_Factura_FechaDoc : 20100101
    #   07_Factura_FechaAsien : 20100101
    #   08_Factura_FechaValor : 20100101
    fecha = xfecha(reg[ "07_Factura_FechaAsien" ])
    
    # cliente -------------------------------------------------------------------------------------
    ctaCliente = xcuenta( reg[ "27_Contab_Tercero" ] )
    nomCliente = reg[ "43_Expedidor_Alias_Empresa" ]
    cifCliente = reg[ "02_Expedidor_CIF" ]
    facNumero = reg[ "04_Factura_Numero" ]
    if len(nomCliente) == 0 :
        error += "Línea %d : falta el nombre del cliente.\r\n"%rg["LINEA"],


    # vencimiento, nos lo inventamos --------------------------------------------------------------
    fvto = empresa.vencimientoCliente( ctaCliente, fecha )

    # importe -------------------------------------------------------------------------------------
    liquido = xfloat(reg["24_Posicion_LiquidoFactura"])

    # Suplidos ------------------------------------------------------------------------------------
    txt = reg["23_OtrosImportes"]
    siSuplidos = False
    if txt and int(txt) :
        importeSuplidos = xfloat(txt)
        ctaSuplidos = xcuenta( reg["32_ContabExpedidor_OtrosImportes"] )
        if not empresa.existeCuenta( ctaSuplidos ) :
            error += "Línea %d : la cuenta %s no está dada de alta\r\n"%(reg["LINEA"], ctaSuplidos)
        else :
            siSuplidos = True

    # Retencion ----------------------------------------------------------------------------------------
    txt = reg["22_Retencion_Cuota"]
    siRetencion = False
    if txt and int(txt) :
        importeRetencion = xfloat(txt)
        ctaRetencion = xcuenta( reg["31_ContabExpedidor_Retencion_Cuota"] )
        if not empresa.existeCuenta( ctaRetencion ) :
            error += "Línea %d : la cuenta %s no está dada de alta\r\n"%(reg["LINEA"], ctaRetencion)
        else :
            vtoRetencion = empresa.vencimientoAutomatico( fecha, "D=20 M+1 A=" )
            siRetencion = True
            

    # ivas ----------------------------------------------------------------------------------------
    liIVAS = []
    def xiva( rg ) :
        txtc = rg["14_ImpuestoIndirecto_Cuota"]
        xerror = ""
        if txtc and int(txtc) and xporc( rg["13_ImpuestoIndirecto_%" ] )>0.00:
            iva = Varios.R()
            iva.base = xfloat( rg["12_ImpuestoIndirecto_BaseImponible"] )
            iva.porc = xporc( rg["13_ImpuestoIndirecto_%" ] )
            iva.cuota = xfloat( txtc )
            iva.dedu = xporc( rg["15_ImpuestoIndirecto_%Deducibilidad"] )
            iva.cta = xcuenta( rg["29_ContabExpedidor_ImpIndirecto_Cuota"] )
            
            txtr = rg["17_Recargo_%"]
            iva.sirecargo = len(txtr) > 0 and int(rg["18_Recargo_Cuota"])
            if iva.sirecargo :
                iva.rec_cuota = xfloat( rg["18_Recargo_Cuota"] )
                iva.rec_porc = xporc( txtr )
                iva.rec_cuenta = xcuenta( rg["30_ContabExpedidor_Recargo_Cuota"] )
            else :
                iva.rec_porc = None
                iva.rec_cuenta = None
                
            iva.numero = empresa.buscaTipoIVAEmitida( iva.cta, iva.porc, iva.rec_cuenta, iva.rec_porc )
            if iva.numero == 0 :
                if iva.sirecargo :
                    xerror = "Línea %d : no existe un tipo de iva repercutido con cta = %s y %0.2f%% + recargo = %s y %0.2f%%\r\n"%(rg["LINEA"],iva.cta,iva.porc,iva.rec_cuenta,iva.rec_porc)
                else :
                    xerror = "Línea %d : no existe un tipo de iva repercutido con cta = %s y %0.2f%%\r\n"%(rg["LINEA"],iva.cta,iva.porc)
            else :
                liIVAS.append( iva )
                    
            #Intracomunitaria
            intracom = rg["33_ContabReceptor_ImpIndirecto_Cuota"]
            if intracom :
                ivaI = Varios.R()
                ivaI.base = -iva.base
                ivaI.porc = iva.porc
                ivaI.cuota = -iva.cuota
                ivaI.dedu = iva.dedu
                ivaI.sirecargo = False
                ivaI.cta = xcuenta( intracom )
                ivaI.numero = -empresa.buscaTipoIVARecibida( ivaI.cta, ivaI.porc, None, None )
                if ivaI.numero == 0 :
                    xerror = "Línea %d : no existe un tipo de iva soportado con cta = %s y %0.2f%%\r\n"%(rg["LINEA"],ivaI.cta,ivaI.porc)                
                else :
                    liIVAS.append( ivaI )
                    
        return xerror
    error += xiva( reg )
    for rg in rmas :
        error += xiva( rg )
    
    ivaMasBase = 0.0
    for iva in liIVAS :
        ivaMasBase += iva.base + iva.cuota
        
    if ivaMasBase == 0.0 : # Añadimos un iva exento
        numExento = empresa.buscaTipoIVAEmitida( "", 0.00, None, None )
        if numExento == 0 :
            error += "Línea %d : no hay ningún iva repercutido exento y es necesario asociarlo a la factura\r\n"%(reg["LINEA"])
        else :
            iva = Varios.R()
            base = liquido
            if siRetencion :
                base += importeRetencion
            if siSuplidos :
                base -= importeSuplidos
            iva.base = base 
            iva.porc = 0.00
            iva.cuota = 0.00
            iva.dedu = 100.00
            iva.sirecargo = False
            iva.cta = ""
            iva.numero = numExento
            liIVAS.append( iva )
    
    # operacion -----------------------------------------------------------------------------------
    liOPS = []
    def xop( rg ) :
        xerror = ""
        txtc = rg["28_Contab_Transaccion"]
        if txtc :
            cuenta = xcuenta( txtc )
            if not empresa.existeCuenta( cuenta ) :
                xerror += "Línea %d : la cuenta %s no está dada de alta\r\n"%(rg["LINEA"], txtc)
                
            importe = xfloat( rg["11_ImporteTransaccion"] )
            for x in liOPS :
                if cuenta == x.cuenta :
                    x.importe += importe
                    return xerror
            op = Varios.R()
            op.importe = importe
            op.cuenta = cuenta
            op.tipo = empresa.buscaTipoEmitida( op.cuenta )
            liOPS.append( op )
        return xerror
    error += xop( reg )
    for rg in rmas :
        error += xop( rg )

    if len(liOPS) == 0 :
        error += "Línea %d : no tiene una operación a la que asignar la factura\r\n"%rg["LINEA"],



    if siSoloErrores :
        return error
        
    
    # Grabamos la factura -------------------------------------------------------------------------
    
    ## Cliente
    dbCuentas = empresa.cuentas
    dbCuentas.comprueba( ctaCliente, nomCliente ) 
    
    dbCli = empresa.clientes
    regCli = dbCli.comprueba( ctaCliente, nomCliente, cifCliente )

    ## Emitidas
    dbEmi = empresa.emitidas

    numero = dbEmi.ultimo() + 1
    dbEmi.append()
    dbEmi.NUMERO = numero
    
    tiponum, cnumero = dbEmi.tipo_cnumero( fecha, liquido )
    dbEmi.TIPONUM = tiponum
    dbEmi.CNUMERO = cnumero

    dbEmi.FECHA = fecha
    dbEmi.FREGISTRO = fecha
    dbEmi.CLIENTE = regCli.NUMERO
    dbEmi.CLCUENTA = regCli.CUENTA
    dbEmi.TOTAL = liquido
    impDT = liquido
    if siRetencion :
        impDT += importeRetencion
    if siSuplidos :
        impDT -= importeSuplidos
    dbEmi.TOTALDECL = impDT
    dbEmi.DECLTERC = "B"

    ### Operaciones
    op = liOPS[0]
    dbEmi.TIPOOP = op.tipo
    dbEmi.TOCUENTA = op.cuenta
    nOps = len(liOPS)
    if nOps > 1 :
        dbAjustes = empresa.ajustes
        for n in range( 1, nOps ) :
            dbAjustes.append()
            dbAjustes.TIPO = "E"
            dbAjustes.NUMERO = numero
            dbAjustes.CUENTA = op.cuenta
            dbAjustes.IMPORTE = op.importe
            dbAjustes.CONTRA = "I"
            dbAjustes.CAMBIOAS = "N"
            dbAjustes.AFECTAIVA = "N"
            dbAjustes.DECLTERC = "N"
        dbAjustes.commit()

    ### Retencion
    if siRetencion :
        dbAjustes = empresa.ajustes
        dbAjustes.append()
        dbAjustes.TIPO = "E"
        dbAjustes.NUMERO = numero
        dbAjustes.CUENTA = ctaRetencion
        dbAjustes.IMPORTE = -importeRetencion
        dbAjustes.CONTRA = "I"
        dbAjustes.CAMBIOAS = "N"
        dbAjustes.AFECTAIVA = "S"
        dbAjustes.DECLTERC = "S"
        dbAjustes.commit()

    ### Suplidos
    if siSuplidos :
        dbAjustes = empresa.ajustes
        dbAjustes.append()
        dbAjustes.TIPO = "E"
        dbAjustes.NUMERO = numero
        dbAjustes.CUENTA = ctaSuplidos
        dbAjustes.IMPORTE = -importeSuplidos
        dbAjustes.CONTRA = "I"
        dbAjustes.CAMBIOAS = "N"
        dbAjustes.AFECTAIVA = "S"
        dbAjustes.DECLTERC = "S"
        dbAjustes.commit()

        

    ### IVA
    dbEriva = empresa.eriva
    for iva in liIVAS :
        no100 = int(iva.dedu) != 100
        cuota = iva.cuota
        base = iva.base
        if no100 :
            cuota = round(cuota*iva.dedu/100.00,2)
            base = round(base*iva.dedu/100.00,2)
            cuotaND = iva.cuota-cuota
            baseND = iva.base-base
        dbEriva.append()
        dbEriva.TIPO = "R"
        dbEriva.FACTURA = numero
        dbEriva.NUMERO = iva.numero
        dbEriva.IVA = iva.porc
        dbEriva.IVA_CTA = iva.cta
        dbEriva.IVA_TOTAL = cuota
        dbEriva.BASE = base
        dbEriva.NODEDU = "N"
        dbEriva.BINVERSION = "N"
        if iva.sirecargo :
            rec_cuota = iva.rec_cuota
            if no100 :
                rec_cuota = round(rec_cuota*iva.dedu/100.00,2)
                rec_cuotaND = iva.rec_cuota-rec_cuota
            dbEriva.RE = iva.rec_porc
            dbEriva.RE_CTA = iva.rec_cuenta
            dbEriva.RE_TOTAL = rec_cuota
            
        if no100 :
            dbEriva.append()
            dbEriva.TIPO = "R"
            dbEriva.FACTURA = numero
            dbEriva.NUMERO = iva.numero
            dbEriva.IVA = iva.porc
            dbEriva.IVA_CTA = iva.cta
            dbEriva.IVA_TOTAL = cuotaND
            dbEriva.BASE = baseND
            dbEriva.NODEDU = "S"
            dbEriva.BINVERSION = "N"
            if iva.sirecargo :
                dbEriva.RE = iva.rec_porc
                dbEriva.RE_CTA = iva.rec_cuenta
                dbEriva.RE_TOTAL = rec_cuotaND
    dbEriva.commit()
            
    ## Vto
    dbVto = empresa.vencimientos
    dbVto.nuevo( "E", numero, fecha, liquido, ctaCliente )
    if siRetencion :
        dbVto.nuevo( "E", numero, vtoRetencion, importeRetencion, ctaCliente, ctaRetencion )
        
    dbVto.commit()
            
    dbEmi.commit()
    
    
    ## Se contabiliza
    dbEmi.contabiliza()

    
#================================================================================================================================================

    
