# -*- coding: latin-1 -*-

import Enlace

import DBFmgd


#---------------------------------------------------------------------------------------------------------------
class Empresa :
    def __init__( self, config, siExclusivo ) :
        Enlace.ponDirEnlace( config.dirBIN )
        self.config = config
        
        self.dllMGD = dllMGD = Enlace.enlaceMGD()
        
        dllMGD.xUsaEmpresa( "S" if siExclusivo else "N", config.empresa )

        self.nombre = Enlace.Zconvierte(dllMGD.leeparametro( "NOMBRE" ))
        self.decimales = int(Enlace.Zconvierte(dllMGD.leeparametro( "DECIMALES" )))
        self.tamcuenta = Enlace.Zconvierte(dllMGD.leeparametro( "TAMCUENTAS" ))

        self.actividad = DBFmgd.Actividad()
        self.analitica = DBFmgd.Analitica()
        self.ajustes = DBFmgd.Ajustes()
        self.bancos = DBFmgd.Bancos()
        self.clientes = DBFmgd.Clientes()
        self.cuentas = DBFmgd.Cuentas()
        self.diario = DBFmgd.Diario()
        self.diariotxt = DBFmgd.DiarioTxt()
        self.directos = DBFmgd.Directos()
        self.emitidas = DBFmgd.Emitidas()
        self.eriva = DBFmgd.Eriva()
        self.eticod = DBFmgd.EtiCod()
        self.etidat = DBFmgd.EtiDat()
        self.exapuntes = DBFmgd.ExApuntes()
        self.explantillas = DBFmgd.ExPlantillas()
        self.extras = DBFmgd.Extras()
        self.formdoc = DBFmgd.Formdoc()
        self.formhoja = DBFmgd.Formhoja()
        self.fotos = DBFmgd.Fotos()
        self.infapun = DBFmgd.Infapun()
        self.informes = DBFmgd.Informes()
        self.lbi = DBFmgd.Lbi()
        self.movbancos = DBFmgd.MovBancos()
        self.pagos = DBFmgd.Pagos()
        self.parametros = DBFmgd.Parametros()
        self.proveedores = DBFmgd.Proveedores()
        self.recibidas = DBFmgd.Recibidas()
        self.recibos = DBFmgd.Recibos()
        self.iva = DBFmgd.IVA()
        self.operaciones = DBFmgd.Operaciones()
        self.referencias = DBFmgd.Referencias()
        self.refapuntes = DBFmgd.RefApuntes()
        self.tipovtos = DBFmgd.TipoVtos()
        self.vencimientos = DBFmgd.Vencimientos()
        self.articulos = DBFmgd.Articulos()
        self.articulosc = DBFmgd.ArticulosC()
        self.familias = DBFmgd.Familias()
        self.familiasc = DBFmgd.FamiliasC()
        self.albemi = DBFmgd.AlbEmi()
        self.albrec = DBFmgd.AlbRec()
        self.albrep = DBFmgd.AlbRep()
        self.albpre = DBFmgd.AlbPre()
        self.albped = DBFmgd.AlbPed()
        self.albpede = DBFmgd.AlbPedE()
        self.albinv = DBFmgd.AlbInv()
        self.apuntes = DBFmgd.Apuntes()

    def cerrar( self ) :
        self.dllMGD.xCerrar( "-" )


    def listaEmpresas( self, dirMGD ) :
        dbemp = self.abreDBF( os.path.join( dirMGD, "comun", "empresas.dbf" ) )
        dbemp.gotop()
        li = []
        class Anonimo :
            pass
        while not dbemp.eof() :
            obj = Anonimo()
            obj.numero = dbemp.fieldget( "NUMERO" )
            obj.nombre = dbemp.fieldget( "NOMBRE" ).strip()
            dbemp.skip(1)
            li.append( obj )
        dbemp.close()
        return li

    def recalculaSaldosBancos( self ) :
        self.dllMGD.recalculasaldos()

    def listaBancos( self ) :
        b = self.bancos
        b.gotop()
        liBancos = []
        while not b.eof() :
            obj = b.regActual()
            if obj.numero > 0 :
                liBancos.append( obj )
            b.skip(1)
        b.close()
        return liBancos

    def tiposIVA( self, tipo ) :
        iva = self.iva
        iva.gotop()
        liTipos = []
        while not iva.eof() :
            obj = iva.regActual()
            if not obj.inactivo and obj.tipo == tipo :
                liTipos.append( obj )
            iva.skip(1)
        iva.close()
        return liTipos

    def tiposIVASoportado( self ) :
        return self.tiposIVA( "S" )

    def tiposIVARepercutido( self ) :
        return self.tiposIVA( "R" )

    def listaCuentas( self ) :
        cta = self.cuentas
        cta.gotop()
        liCuentas = []
        while not cta.eof() :
            liCuentas.append( cta.regActual() )
            cta.skip(1)
        cta.close()
        return liCuentas
        
    def existeCuenta( self, cuenta ) :
        self.cuentas.indiceCUENTA()
        return self.cuentas.seek( cuenta )

    def tiposOperacion( self, tipo ) :
        op = self.operaciones
        op.gotop()
        liTipos = []
        while not op.eof() :
            obj = op.regActual()
            if obj.tipo == tipo :
                liTipos.append( obj )
            op.skip(1)
        op.close()
        return liTipos

    def tiposProveedores( self ) :
        return self.tiposOperacion( "P" )

    def tiposClientes( self ) :
        return self.tiposOperacion( "C" )

    def tiposRecibidas( self ) :
        return self.tiposOperacion( "R" )

    def tiposEmitidas( self ) :
        return self.tiposOperacion( "E" )

    def recNombreProveedor( self ) :
        self.proveedores.indiceNUMERO()
        if self.proveedores.seek( self.recibidas.proveedor() ) :
            return self.proveedores.nombre()
        else :
            return ""
            
    def vencimientoCliente( self, cuenta, fecha ) :
        zfecha = Enlace.convierteZ( fecha )
        zcuenta = Enlace.convierteZ( cuenta )
        return Enlace.Zconvierte(self.dllMGD.vencimientoCliente( zcuenta, zfecha ))
    def vencimientoProveedor( self, cuenta, fecha ) :
        zfecha = Enlace.convierteZ( fecha )
        zcuenta = Enlace.convierteZ( cuenta )
        return Enlace.Zconvierte(self.dllMGD.vencimientoProveedor( zcuenta, zfecha ))
    
    def vencimientoAutomatico( self, fecha, orden ) :
        zfecha = Enlace.convierteZ( fecha )
        zorden = Enlace.convierteZ( orden )
        return Enlace.Zconvierte(self.dllMGD.vencimientoAutomatico( zfecha, zorden ))
        
    def _buscaTipoOP( self, cuenta, er ) :
        op = self.operaciones
        op.gotop()
        while not op.eof() :
            if op.TIPO == er and self.mismaCuenta( op.CUENTA, cuenta ) :
                return op.NUMERO
            op.skip(1)
        return 0

    def buscaTipoRecibida( self, cuenta ) :
        return self._buscaTipoOP( cuenta, "R" )
    def buscaTipoEmitida( self, cuenta ) :
        return self._buscaTipoOP( cuenta, "E" )

    def _buscaTipoIVA( self, tipo, cuenta, porc, cta_rec, porc_rec ) :
        iva = self.iva
        iva.gotop()
        while not iva.eof() :
            
            if iva.TIPO == tipo and self.mismaCuenta(iva.CTA_IVA, cuenta) and self.mismoFloat(iva.IVA, porc) :
                if cta_rec :
                    if self.mismaCuenta(iva.CTA_IVA_RE, cta_rec) and self.mismoFloat(iva.IVA_RE, porc_rec) :
                        return iva.NUMERO
                else :
                    return iva.NUMERO
            iva.skip(1)
        return 0

    def buscaTipoIVARecibida( self, cuenta, porc, cta_rec, porc_rec ) :
        return self._buscaTipoIVA( "S", cuenta, porc, cta_rec, porc_rec )
        

    def buscaTipoIVAEmitida( self, cuenta, porc, cta_rec, porc_rec ) :
        return self._buscaTipoIVA( "R", cuenta, porc, cta_rec, porc_rec )
        
    def mismaCuenta( self, cta1, cta2 ) :
        if cta1.strip() == "" :
            return cta1.strip() == cta2.strip()
        tc = self.tamcuenta
        cta1 = cta1[:tc]
        cta2 = cta2[:tc]
        return cta1 == cta2
    
    def mismoFloat( self, imp1, imp2 ) :
        return abs( imp1-imp2 ) < 0.001

#---------------------------------------------------------------------------------------------------------------
