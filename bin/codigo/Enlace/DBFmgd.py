# -*- coding: latin-1 -*-
import DBFmgdGen

#===================================================================================================================
class Actividad( DBFmgdGen.ActividadBase ) :
    pass
#===================================================================================================================
class Analitica( DBFmgdGen.AnaliticaBase ) :
    pass
#===================================================================================================================
class Ajustes( DBFmgdGen.AjustesBase ) :
    pass
#===================================================================================================================
class Bancos( DBFmgdGen.BancosBase ) :
    def numBanco( self, cuenta ) :
        self.gotop()
        while not self.eof() :
            if cuenta == self.cuenta() :
                return self.NUMERO
            self.skip(1)
        return 0
#===================================================================================================================
class Clientes( DBFmgdGen.ClientesBase ) :
    def comprueba( self, cuenta, nombre, nif ) :
        self.indiceCUENTA()
        if not self.seek( cuenta ) :
            numero = self.ultimo() + 1
            self.append()
            self.CUENTA = cuenta
            self.NUMERO = numero
            self.NOMBRE = nombre
            self.NIF = nif
        else :
            if not self.NOMBRE.startswith(nombre) :
                self.NOMBRE = nombre
            if self.NIF.strip() != nif.strip() :
                self.NIF = nif
        self.commit()
        return self.regActual()

#===================================================================================================================
class Cuentas( DBFmgdGen.CuentasBase ) :
    def comprueba( self, cuenta, nombre ) :
        self.indiceCUENTA()
        if not self.seek( cuenta ) :
            self.append()
            self.CUENTA = cuenta
            self.TEXTO = nombre
        else :
            txt = nombre.strip()
            if txt and self.TEXTO.strip() != txt :
                self.TEXTO = txt
        self.commit()
        return self.regActual()
#===================================================================================================================
class Diario( DBFmgdGen.DiarioBase ) :
    pass
#===================================================================================================================
class DiarioTxt( DBFmgdGen.DiarioTxtBase ) :
    pass
#===================================================================================================================
class Directos( DBFmgdGen.DirectosBase ) :
    pass
#===================================================================================================================
class Emitidas( DBFmgdGen.EmitidasBase ) :
    def nueva( self, fecha, total, baseImponible, regCliente, regIVA, regOperacion, opcuenta ) :
        numero = self.ultimo() + 1
        self.append()
        self.NUMERO = numero

        tiponum, cnumero = self.tipo_cnumero( fecha, total )
        self.TIPONUM = tiponum
        self.CNUMERO = cnumero

        self.FECHA = fecha
        self.FREGISTRO = fecha
        self.CLIENTE = regCliente.NUMERO
        self.CLCUENTA = regCliente.CUENTA 

        if regOperacion :
            self.TIPOOP = regOperacion.NUMERO
        self.TOCUENTA = opcuenta

        self.TOTAL = total
        self.TOTALDECL = total
        self.DECLTERC = "B"

        self.commit()

        return numero

    def numFactura( self ) :
        return self.access( "NUMEXTERNO" )

#===================================================================================================================
class Eriva( DBFmgdGen.ErivaBase ) :

    def nuevo( self, tipo, factura, baseImponible, impIVA, regIVA ) :

        self.append()
        self.TIPO = tipo
        self.FACTURA = factura
        self.NUMERO = regIVA.numero
        self.IVA = regIVA.iva
        self.IVA_CTA = regIVA.cta_iva
        self.IVA_TOTAL = impIVA
        self.BASE = baseImponible
        self.NODEDU = "N"
        self.BINVERSION = "N"

        self.commit()

#===================================================================================================================
class EtiCod( DBFmgdGen.EtiCodBase ) :
    pass
#===================================================================================================================
class EtiDat( DBFmgdGen.EtiDatBase ) :
    pass
#===================================================================================================================
class ExApuntes( DBFmgdGen.ExApuntesBase ) :
    def nuevo( self, extra, concepto, cuenta, importe ) :
        numero = self.ultimo() + 1
        self.append()
        self.NUMERO = numero 

        self.EXTRA = extra 
        self.CUENTA = cuenta 
        self.AYUDA = concepto 
        self.DH = "D" if importe > 0.0001 else "H" 
        self.IMPORTE = abs(importe )
        self.commit()

        return numero
#===================================================================================================================
class ExPlantillas( DBFmgdGen.ExPlantillasBase ) :
    pass
#===================================================================================================================
class Extras( DBFmgdGen.ExtrasBase ) :
    def nuevo( self, fecha, concepto ) :
        numero = self.ultimo() + 1
        self.append()
        self.NUMERO = numero

        tiponum, cnumero = self.tipo_cnumero( fecha, 0.00 )
        self.TIPONUM = tiponum 
        self.CNUMERO = cnumero 

        self.FECHA = fecha 
        self.TIPO = "M"
        self.TEXTO = concepto 
        self.commit()

        return numero

    def numExterno( self ) :
        return self.access( "NUMEXTERNO" )

#===================================================================================================================
class Formdoc( DBFmgdGen.FormdocBase ) :
    pass
#===================================================================================================================
class Formhoja( DBFmgdGen.FormhojaBase ) :
    pass
#===================================================================================================================
class Fotos( DBFmgdGen.FotosBase ) :
    pass
#===================================================================================================================
class Infapun( DBFmgdGen.InfapunBase ) :
    pass
#===================================================================================================================
class Informes( DBFmgdGen.InformesBase ) :
    pass
#===================================================================================================================
class Lbi( DBFmgdGen.LbiBase ) :
    pass
#===================================================================================================================
class MovBancos( DBFmgdGen.MovBancosBase ) :
    def nuevo( self, numBanco, fecha, concepto, total ) :
        numero = self.ultimo() + 1
        self.append()
        self.BANCO = numBanco 
        self.NUMERO = numero 

        tiponum, cnumero = self.tipo_cnumero( fecha, total )
        self.TIPONUM = tiponum
        self.CNUMERO = cnumero

        self.FECHA = fecha
        self.TEXTO = concepto
        self.CLAVE = "ZZZ"

        self.TOTAL = total

        self.commit()

        return numero

    def trasvase( self, dbpagos, numBanco1, numBanco2, fecha, concepto, importe, cuenta2 ) :
        numero = self.ultimo() + 1
        self.append()
        self.FECHA = fecha
        self.BANCO = numBanco1
        self.NUMERO = numero

        tiponum, cnumero = self.tipo_cnumero( fecha, importe )
        self.TIPONUM = tiponum
        self.CNUMERO = cnumero

        self.TEXTO = concepto
        self.TOTAL = importe
        self.CLAVE = "ZZZ"

        self.commit()

        self.append()
        self.FECHA = fecha
        self.BANCO = numBanco2
        self.NUMERO = numero + 1

        self.TIPONUM = tiponum
        self.CNUMERO = cnumero + 1

        self.TEXTO = concepto
        self.TOTAL = -importe
        self.CLAVE = "ZZZ"

        self.commit()

        dbpagos.append()
        dbpagos.BANCO = numBanco1
        dbpagos.NUMERO = numero + 1
        dbpagos.IMPORTE = -importe
        dbpagos.DIRSUBCTA = cuenta2
        dbpagos.NUMEROT = numero
        dbpagos.BANCOT = numBanco2
        dbpagos.commit()

        dbpagos.append()
        dbpagos.BANCO = numBanco2
        dbpagos.NUMERO = numero
        dbpagos.IMPORTE = importe
        dbpagos.DIRSUBCTA = cuenta2
        dbpagos.NUMEROT = numero+1
        dbpagos.BANCOT = numBanco1
        dbpagos.commit()

    def numExterno( self ) :
        return self.access( "NUMEXTERNO" )

#===================================================================================================================
class Pagos( DBFmgdGen.PagosBase ) :
    def nuevoCuenta( self, numBanco, numero, importe, cuenta ) :
        self.append()
        self.BANCO = numBanco
        self.NUMERO = numero
        self.IMPORTE = importe
        self.DIRSUBCTA = cuenta
        self.commit()

    def nuevoVencimiento( self, numBanco, numero, importe, vto ) :
        self.append()
        self.BANCO = numBanco
        self.NUMERO = numero
        self.IMPORTE = importe
        self.VTO = vto
        self.commit()

#===================================================================================================================
class Parametros( DBFmgdGen.ParametrosBase ) :
    pass
#===================================================================================================================
class Proveedores( DBFmgdGen.ProveedoresBase ) :
    def comprueba( self, cuenta, nombre, nif ) :
        self.indiceCUENTA()
        if not self.seek( cuenta ) :
            numero = self.ultimo() + 1
            self.append()
            self.CUENTA = cuenta
            self.NUMERO = numero
            self.NOMBRE = nombre
            self.NIF = nif
        else :
            if self.NOMBRE.strip() != nombre :
                self.NOMBRE = nombre
            if self.NIF.strip() != nif.strip() :
                self.NIF = nif
        self.commit()
        return self.regActual()

#===================================================================================================================
class Recibidas( DBFmgdGen.RecibidasBase ) :

    def nueva( self, fecha, total, regProveedor, regIVA, regOperacion, opcuenta ) :
        numero = self.ultimo() + 1
        self.append()
        self.NUMERO = numero

        tiponum, cnumero = self.tipo_cnumero( fecha, total )
        self.TIPONUM = tiponum
        self.CNUMERO = cnumero

        self.FECHA = fecha
        self.REGFECHA = fecha
        self.PROVEEDOR = regProveedor.NUMERO
        self.PRCUENTA = regProveedor.CUENTA
        self.PRFECHA = fecha

        if regOperacion :
            self.TIPOOP = regOperacion.NUMERO
        self.TOCUENTA = opcuenta

        self.TOTAL = total
        self.TOTALDECL = total
        self.DECLTERC = "B"

        self.commit()

        return numero

    def numFactura( self ) :
        return self.access( "NUMEXTERNO" )
        
    def siRepetida( self, numProveedor, prFactura ) :
        self.indiceREPETIDA()
        return self.seek( "%-20s%5d"%( prFactura, numProveedor ) )

#===================================================================================================================
class Recibos( DBFmgdGen.RecibosBase ) :
    pass
#===================================================================================================================
class IVA( DBFmgdGen.IVABase ) :
    def buscaNumero( self, tipo, cuenta ) :
        self.gotop()
        while not self.eof() :
            if not self.INACTIVO and self.TIPO == tipo and self.CTA_IVA == cuenta :
                return self.regActual()
            self.skip(1)
        return None
#===================================================================================================================
class Operaciones( DBFmgdGen.OperacionesBase ) :
    def buscaNumero( self, tipo, cuenta ) :
        self.gotop()
        while not self.eof() :
            if self.TIPO == tipo and self.CUENTA == cuenta:
                return self.regActual()
            self.skip(1)
        return None
#===================================================================================================================
class Referencias( DBFmgdGen.ReferenciasBase ) :
    pass
#===================================================================================================================
class RefApuntes( DBFmgdGen.RefApuntesBase ) :
    pass
#===================================================================================================================
class TipoVtos( DBFmgdGen.TipoVtosBase ) :
    pass

#===================================================================================================================
class Vencimientos( DBFmgdGen.VencimientosBase ) :
    def nuevo( self, tipo, tpnumero, fecha, importe, cuentadef, cuenta = None ) :

        numero = self.ultimo() + 1
        self.append()
        self.NUMERO = numero

        self.TIPO = tipo
        self.TPNUMERO = tpnumero
        self.FECHA = fecha
        self.IMPORTE = importe
        self.PENDIENTE = importe
        self.CUENTADEF = cuentadef
        if cuenta :
            self.CUENTA = cuenta
        self.commit()

    def buscaPendiente( self, cuenta, pendiente ) :
        self.indicePENDIENTE()
        if self.seek( pendiente ) :
            while not self.eof() :
                if cuenta == self.CUENTADEF or cuenta == self.CUENTA :
                    return self.NUMERO
                self.skip(1)
                if pendiente != self.PENDIENTE :
                    break
        return 0

#===================================================================================================================
class Articulos( DBFmgdGen.ArticulosBase ) :
    pass
#===================================================================================================================
class ArticulosC( DBFmgdGen.ArticulosCBase ) :
    pass
#===================================================================================================================
class Familias( DBFmgdGen.FamiliasBase ) :
    pass
#===================================================================================================================
class FamiliasC( DBFmgdGen.FamiliasCBase ) :
    pass
#===================================================================================================================
class AlbEmi( DBFmgdGen.AlbEmiBase ) :
    pass
#===================================================================================================================
class AlbRec( DBFmgdGen.AlbRecBase ) :
    pass
#===================================================================================================================
class AlbRep( DBFmgdGen.AlbRepBase ) :
    pass
#===================================================================================================================
class AlbPre( DBFmgdGen.AlbPreBase ) :
    pass
#===================================================================================================================
class AlbPed( DBFmgdGen.AlbPedBase ) :
    pass
#===================================================================================================================
class AlbPedE( DBFmgdGen.AlbPedEBase ) :
    pass
#===================================================================================================================
class AlbInv( DBFmgdGen.AlbInvBase ) :
    pass
#===================================================================================================================
class Apuntes( DBFmgdGen.ApuntesBase ) :
    pass
