# -*- coding: latin-1 -*-

import DBFexten

class Anonimo :
    pass

class ActividadBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 45 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.NOMBRE = self.fieldget( 'NOMBRE' ).rstrip()
        obj.ETIQUETA = self.fieldget( 'ETIQUETA' ).rstrip()
        obj.ACTIVA = self.fieldget( 'ACTIVA' ).rstrip()
        return obj


class AnaliticaBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 46 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.CUENTA = self.fieldget( 'CUENTA' ).rstrip()
        obj.ACTIVIDAD = self.fieldget( 'ACTIVIDAD' )
        obj.IMPORTE = self.fieldget( 'IMPORTE' )
        return obj

    def indiceTNUMERO( self ) :
        self.setorder( 'TNUMERO' ) # TIPO+STR(NUMERO,10)+CUENTA+STR(ACTIVIDAD,2)

class AjustesBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 27 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.CUENTA = self.fieldget( 'CUENTA' ).rstrip()
        obj.IMPORTE = self.fieldget( 'IMPORTE' )
        obj.CONTRA = self.fieldget( 'CONTRA' ).rstrip()
        obj.CAMBIOAS = self.fieldget( 'CAMBIOAS' ).rstrip()
        obj.AFECTAIVA = self.fieldget( 'AFECTAIVA' ).rstrip()
        obj.DECLTERC = self.fieldget( 'DECLTERC' ).rstrip()
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # TIPO+STR(NUMERO,8)

class BancosBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 1 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.NOMBRE = self.fieldget( 'NOMBRE' ).rstrip()
        obj.SUCURSAL = self.fieldget( 'SUCURSAL' ).rstrip()
        obj.NUMCTA = self.fieldget( 'NUMCTA' ).rstrip()
        obj.CUENTA = self.fieldget( 'CUENTA' ).rstrip()
        obj.SALDOINI = self.fieldget( 'SALDOINI' )
        obj.SALDOACT = self.fieldget( 'SALDOACT' )
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceNOMBRE( self ) :
        self.setorder( 'NOMBRE' ) # NOMBRE

class ClientesBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 2 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.NOMBRE = self.fieldget( 'NOMBRE' ).rstrip()
        obj.COMERCIAL = self.fieldget( 'COMERCIAL' ).rstrip()
        obj.DOMICILIO = self.fieldget( 'DOMICILIO' ).rstrip()
        obj.LOCALIDAD = self.fieldget( 'LOCALIDAD' ).rstrip()
        obj.PROVINCIA = self.fieldget( 'PROVINCIA' ).rstrip()
        obj.COD_POSTAL = self.fieldget( 'COD_POSTAL' ).rstrip()
        obj.AP_CORREOS = self.fieldget( 'AP_CORREOS' ).rstrip()
        obj.NIF = self.fieldget( 'NIF' ).rstrip()
        obj.CUENTA = self.fieldget( 'CUENTA' ).rstrip()
        obj.OPERACION = self.fieldget( 'OPERACION' )
        obj.BRUTO = self.fieldget( 'BRUTO' )
        obj.NETO = self.fieldget( 'NETO' )
        obj.PENDIENTE = self.fieldget( 'PENDIENTE' )
        obj.BANCO_NOM = self.fieldget( 'BANCO_NOM' ).rstrip()
        obj.BANCO_SUC = self.fieldget( 'BANCO_SUC' ).rstrip()
        obj.BANCO_DIG = self.fieldget( 'BANCO_DIG' ).rstrip()
        obj.IVA = self.fieldget( 'IVA' )
        obj.BANCO_TIT = self.fieldget( 'BANCO_TIT' ).rstrip()
        obj.ANTICIPO = self.fieldget( 'ANTICIPO' ).rstrip()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.DECLTERC = self.fieldget( 'DECLTERC' ).rstrip()
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        obj.CONTACTOS = self.fieldget( 'CONTACTOS' )
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceNOMBRE( self ) :
        self.setorder( 'NOMBRE' ) # UPPER(NOMBRE)
    def indiceCOMERCIAL( self ) :
        self.setorder( 'COMERCIAL' ) # UPPER(COMERCIAL)
    def indiceBRUTO( self ) :
        self.setorder( 'BRUTO' ) # BRUTO
    def indiceCUENTA( self ) :
        self.setorder( 'CUENTA' ) # CUENTA

class CuentasBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 3 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.CUENTA = self.fieldget( 'CUENTA' ).rstrip()
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        obj.DEBE = self.fieldget( 'DEBE' )
        obj.HABER = self.fieldget( 'HABER' )
        obj.PENTIDAD = self.fieldget( 'PENTIDAD' )
        obj.PDIRECTO = self.fieldget( 'PDIRECTO' )
        obj.PTIPO = self.fieldget( 'PTIPO' )
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        return obj

    def indiceCUENTA( self ) :
        self.setorder( 'CUENTA' ) # CUENTA
    def indiceTEXTO( self ) :
        self.setorder( 'TEXTO' ) # TEXTO

class DiarioBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 17 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.ASIENTO = self.fieldget( 'ASIENTO' )
        obj.FECHA = self.fieldget( 'FECHA' )
        obj.TPASIENTO = self.fieldget( 'TPASIENTO' ).rstrip()
        obj.CLAVE = self.fieldget( 'CLAVE' ).rstrip()
        obj.CLAVE_ORI = self.fieldget( 'CLAVE_ORI' ).rstrip()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.IMPORTE = self.fieldget( 'IMPORTE' )
        obj.CUENTA = self.fieldget( 'CUENTA' ).rstrip()
        obj.SALDO = self.fieldget( 'SALDO' )
        obj.MULTI = self.fieldget( 'MULTI' ).rstrip()
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        return obj

    def indiceFECHA( self ) :
        self.setorder( 'FECHA' ) # DTOS(FECHA)+STR(ASIENTO,10)
    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # TIPO+STR(NUMERO,10)+MULTI
    def indiceCUENTA( self ) :
        self.setorder( 'CUENTA' ) # CUENTA+DTOS(FECHA)+STR(ASIENTO,10)
    def indiceTPASIENTO( self ) :
        self.setorder( 'TPASIENTO' ) # DTOS(FECHA)+TPASIENTO,TPASIENT
    def indiceASIENTO( self ) :
        self.setorder( 'ASIENTO' ) # STR(YEAR(FECHA),4)+STR(ASIENTO,10),EMPTY(CUENTA

class DiarioTxtBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 18 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.CUENTA = self.fieldget( 'CUENTA' ).rstrip()
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        obj.DOCU = self.fieldget( 'DOCU' ).rstrip()
        obj.MULTI = self.fieldget( 'MULTI' ).rstrip()
        obj.NEGATIVO = self.fieldget( 'NEGATIVO' ).rstrip()
        obj.ACUMULAR = self.fieldget( 'ACUMULAR' ).rstrip()
        obj.FECHA = self.fieldget( 'FECHA' )
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # TIPO+STR(NUMERO,10)+MULTI+CUENTA

class DirectosBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 39 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.CUENTA = self.fieldget( 'CUENTA' ).rstrip()
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        return obj


class EmitidasBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 4 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.CNUMERO = self.fieldget( 'CNUMERO' )
        obj.TIPONUM = self.fieldget( 'TIPONUM' ).rstrip()
        obj.CNUMALT = self.fieldget( 'CNUMALT' ).rstrip()
        obj.FECHA = self.fieldget( 'FECHA' )
        obj.FREGISTRO = self.fieldget( 'FREGISTRO' )
        obj.CLIENTE = self.fieldget( 'CLIENTE' )
        obj.CLCUENTA = self.fieldget( 'CLCUENTA' ).rstrip()
        obj.TIPOOP = self.fieldget( 'TIPOOP' )
        obj.TOCUENTA = self.fieldget( 'TOCUENTA' ).rstrip()
        obj.TOTAL = self.fieldget( 'TOTAL' )
        obj.TOTALDECL = self.fieldget( 'TOTALDECL' )
        obj.DECLTERC = self.fieldget( 'DECLTERC' ).rstrip()
        obj.ESTADO = self.fieldget( 'ESTADO' ).rstrip()
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        obj.REGISTRO = self.fieldget( 'REGISTRO' )
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceCNUMERO( self ) :
        self.setorder( 'CNUMERO' ) # STR(YEAR(FECHA),4)+TIPONUM+STR(CNUMERO,9)
    def indiceCLIENTE( self ) :
        self.setorder( 'CLIENTE' ) # CLIENTE
    def indiceFECHA( self ) :
        self.setorder( 'FECHA' ) # DTOS(FECHA)+TIPONUM+STR(CNUMERO,9)

class ErivaBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 22 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.FACTURA = self.fieldget( 'FACTURA' )
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.IVA = self.fieldget( 'IVA' )
        obj.IVA_CTA = self.fieldget( 'IVA_CTA' ).rstrip()
        obj.IVA_TOTAL = self.fieldget( 'IVA_TOTAL' )
        obj.RE = self.fieldget( 'RE' )
        obj.RE_CTA = self.fieldget( 'RE_CTA' ).rstrip()
        obj.RE_TOTAL = self.fieldget( 'RE_TOTAL' )
        obj.BASE = self.fieldget( 'BASE' )
        obj.NODEDU = self.fieldget( 'NODEDU' ).rstrip()
        obj.BINVERSION = self.fieldget( 'BINVERSION' ).rstrip()
        return obj

    def indiceFACTURA( self ) :
        self.setorder( 'FACTURA' ) # TIPO+STR(FACTURA,8)

class EtiCodBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 41 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.CLAVE = self.fieldget( 'CLAVE' ).rstrip()
        obj.FORMA = self.fieldget( 'FORMA' ).rstrip()
        obj.CODIGO = self.fieldget( 'CODIGO' ).rstrip()
        return obj


class EtiDatBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 42 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.CLAVE = self.fieldget( 'CLAVE' ).rstrip()
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        return obj

    def indiceTNUMERO( self ) :
        self.setorder( 'TNUMERO' ) # TIPO+STR(NUMERO,10)+CLAVE

class ExApuntesBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 5 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.EXTRA = self.fieldget( 'EXTRA' )
        obj.CUENTA = self.fieldget( 'CUENTA' ).rstrip()
        obj.AYUDA = self.fieldget( 'AYUDA' ).rstrip()
        obj.DH = self.fieldget( 'DH' ).rstrip()
        obj.IMPORTE = self.fieldget( 'IMPORTE' )
        obj.DECLTERC = self.fieldget( 'DECLTERC' ).rstrip()
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceEXTRA( self ) :
        self.setorder( 'EXTRA' ) # EXTRA

class ExPlantillasBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 6 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        obj.CONTENIDO = self.fieldget( 'CONTENIDO' )
        return obj

    def indiceTEXTO( self ) :
        self.setorder( 'TEXTO' ) # TEXTO

class ExtrasBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 7 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.CNUMERO = self.fieldget( 'CNUMERO' )
        obj.TIPONUM = self.fieldget( 'TIPONUM' ).rstrip()
        obj.CNUMALT = self.fieldget( 'CNUMALT' ).rstrip()
        obj.FECHA = self.fieldget( 'FECHA' )
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.CLAVE = self.fieldget( 'CLAVE' ).rstrip()
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        obj.GRUPO = self.fieldget( 'GRUPO' ).rstrip()
        obj.ESTADO = self.fieldget( 'ESTADO' ).rstrip()
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceCNUMERO( self ) :
        self.setorder( 'CNUMERO' ) # STR(YEAR(FECHA),4)+TIPONUM+STR(CNUMERO,9)
    def indiceFECHA( self ) :
        self.setorder( 'FECHA' ) # DTOS(FECHA)+TIPO+CLAVE

class FormdocBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 23 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        obj.ENBLANCO = self.fieldget( 'ENBLANCO' )
        obj.COPIAS = self.fieldget( 'COPIAS' )
        obj.DATOS = self.fieldget( 'DATOS' )
        return obj


class FormhojaBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 24 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        obj.DATOS = self.fieldget( 'DATOS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # TIPO+STR(NUMERO,3)
    def indiceTEXTO( self ) :
        self.setorder( 'TEXTO' ) # TIPO+TEXTO

class FotosBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 44 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.NOMBRE = self.fieldget( 'NOMBRE' ).rstrip()
        obj.MOSTRAR = self.fieldget( 'MOSTRAR' )
        obj.IZQ = self.fieldget( 'IZQ' )
        obj.ARR = self.fieldget( 'ARR' )
        obj.ANCHO = self.fieldget( 'ANCHO' )
        obj.ALTO = self.fieldget( 'ALTO' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # TIPO+STR(NUMERO,8)

class InfapunBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 20 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.INFORME = self.fieldget( 'INFORME' )
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.PADRE = self.fieldget( 'PADRE' )
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        obj.TIPO = self.fieldget( 'TIPO' )
        obj.MODO_IMP = self.fieldget( 'MODO_IMP' )
        obj.LINEA_SEP = self.fieldget( 'LINEA_SEP' )
        obj.LINEA_DEB = self.fieldget( 'LINEA_DEB' )
        obj.LINEA_ENC = self.fieldget( 'LINEA_ENC' )
        obj.CONDICION = self.fieldget( 'CONDICION' )
        obj.MARGEN_TXT = self.fieldget( 'MARGEN_TXT' )
        obj.MARGEN_IMP = self.fieldget( 'MARGEN_IMP' )
        obj.ALIN_TXT = self.fieldget( 'ALIN_TXT' )
        obj.ALIN_IMP = self.fieldget( 'ALIN_IMP' )
        obj.CLAVE = self.fieldget( 'CLAVE' ).rstrip()
        obj.DECIMALES = self.fieldget( 'DECIMALES' )
        obj.SUMAR = self.fieldget( 'SUMAR' )
        obj.NEGRITA = self.fieldget( 'NEGRITA' )
        obj.HABER = self.fieldget( 'HABER' )
        obj.PORC = self.fieldget( 'PORC' ).rstrip()
        obj.TIPOSAS = self.fieldget( 'TIPOSAS' ).rstrip()
        obj.DATOS = self.fieldget( 'DATOS' )
        return obj

    def indiceINFORME( self ) :
        self.setorder( 'INFORME' ) # INFORME

class InformesBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 19 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.NOMBRE = self.fieldget( 'NOMBRE' ).rstrip()
        obj.TITULO = self.fieldget( 'TITULO' ).rstrip()
        obj.PGC = self.fieldget( 'PGC' ).rstrip()
        obj.ANCHO_TXT = self.fieldget( 'ANCHO_TXT' )
        obj.SI_MULTI = self.fieldget( 'SI_MULTI' )
        obj.CABECERA = self.fieldget( 'CABECERA' ).rstrip()
        obj.TIPOS = self.fieldget( 'TIPOS' ).rstrip()
        obj.CLAVE = self.fieldget( 'CLAVE' ).rstrip()
        obj.COMPROBAR = self.fieldget( 'COMPROBAR' )
        obj.COLUMNAS = self.fieldget( 'COLUMNAS' )
        obj.PROGRAMA = self.fieldget( 'PROGRAMA' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceNOMBRE( self ) :
        self.setorder( 'NOMBRE' ) # NOMBRE

class LbiBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 26 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NOMBRE = self.fieldget( 'NOMBRE' ).rstrip()
        obj.CUENBIEN = self.fieldget( 'CUENBIEN' ).rstrip()
        obj.CUENDOTA = self.fieldget( 'CUENDOTA' ).rstrip()
        obj.CUENAMORT = self.fieldget( 'CUENAMORT' ).rstrip()
        obj.COSTE = self.fieldget( 'COSTE' )
        obj.RESIDUAL = self.fieldget( 'RESIDUAL' )
        obj.FECHA = self.fieldget( 'FECHA' )
        obj.FBAJA = self.fieldget( 'FBAJA' )
        obj.CBAJA = self.fieldget( 'CBAJA' ).rstrip()
        obj.COEFI = self.fieldget( 'COEFI' )
        obj.PERIODO = self.fieldget( 'PERIODO' )
        obj.MESES = self.fieldget( 'MESES' )
        obj.IVA = self.fieldget( 'IVA' )
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        obj.RECIBIDA = self.fieldget( 'RECIBIDA' )
        obj.PROVEEDOR = self.fieldget( 'PROVEEDOR' )
        obj.REGFECHA = self.fieldget( 'REGFECHA' )
        obj.REGISTRO = self.fieldget( 'REGISTRO' )
        obj.CUADRO = self.fieldget( 'CUADRO' )
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNOMBRE( self ) :
        self.setorder( 'NOMBRE' ) # NOMBRE
    def indiceFECHA( self ) :
        self.setorder( 'FECHA' ) # DTOS(FECHA)+NOMBRE
    def indiceCUENTA( self ) :
        self.setorder( 'CUENTA' ) # CUENBIEN

class MovBancosBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 9 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.BANCO = self.fieldget( 'BANCO' )
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.CNUMERO = self.fieldget( 'CNUMERO' )
        obj.TIPONUM = self.fieldget( 'TIPONUM' ).rstrip()
        obj.CNUMALT = self.fieldget( 'CNUMALT' ).rstrip()
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        obj.AUTOTEXT = self.fieldget( 'AUTOTEXT' )
        obj.CLAVE = self.fieldget( 'CLAVE' ).rstrip()
        obj.FECHA = self.fieldget( 'FECHA' )
        obj.TOTAL = self.fieldget( 'TOTAL' )
        obj.SALDONUE = self.fieldget( 'SALDONUE' )
        obj.ESTADO = self.fieldget( 'ESTADO' ).rstrip()
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceCNUMERO( self ) :
        self.setorder( 'CNUMERO' ) # STR(100+BANCO,3)+STR(YEAR(FECHA),4)+TIPONUM+STR(CNUMERO,9)
    def indiceFECHA( self ) :
        self.setorder( 'FECHA' ) # STR(100+BANCO,3)+DTOS(FECHA)+CLAVE

class PagosBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 11 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.BANCO = self.fieldget( 'BANCO' )
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.IMPORTE = self.fieldget( 'IMPORTE' )
        obj.VTO = self.fieldget( 'VTO' )
        obj.DIRSUBCTA = self.fieldget( 'DIRSUBCTA' ).rstrip()
        obj.NUMEROT = self.fieldget( 'NUMEROT' )
        obj.BANCOT = self.fieldget( 'BANCOT' )
        obj.DECLTERC = self.fieldget( 'DECLTERC' ).rstrip()
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceVTO( self ) :
        self.setorder( 'VTO' ) # VTO

class ParametrosBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 12 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.ETIQUETA = self.fieldget( 'ETIQUETA' ).rstrip()
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        obj.MAS = self.fieldget( 'MAS' )
        return obj


class ProveedoresBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 13 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.NOMBRE = self.fieldget( 'NOMBRE' ).rstrip()
        obj.COMERCIAL = self.fieldget( 'COMERCIAL' ).rstrip()
        obj.DOMICILIO = self.fieldget( 'DOMICILIO' ).rstrip()
        obj.LOCALIDAD = self.fieldget( 'LOCALIDAD' ).rstrip()
        obj.PROVINCIA = self.fieldget( 'PROVINCIA' ).rstrip()
        obj.COD_POSTAL = self.fieldget( 'COD_POSTAL' ).rstrip()
        obj.AP_CORREOS = self.fieldget( 'AP_CORREOS' ).rstrip()
        obj.NIF = self.fieldget( 'NIF' ).rstrip()
        obj.CUENTA = self.fieldget( 'CUENTA' ).rstrip()
        obj.OPERACION = self.fieldget( 'OPERACION' )
        obj.BRUTO = self.fieldget( 'BRUTO' )
        obj.PENDIENTE = self.fieldget( 'PENDIENTE' )
        obj.NETO = self.fieldget( 'NETO' )
        obj.IVA = self.fieldget( 'IVA' )
        obj.CTAIRPF = self.fieldget( 'CTAIRPF' ).rstrip()
        obj.ANTICIPO = self.fieldget( 'ANTICIPO' ).rstrip()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.DECLTERC = self.fieldget( 'DECLTERC' ).rstrip()
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        obj.CONTACTOS = self.fieldget( 'CONTACTOS' )
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceNOMBRE( self ) :
        self.setorder( 'NOMBRE' ) # UPPER(NOMBRE)
    def indiceCOMERCIAL( self ) :
        self.setorder( 'COMERCIAL' ) # UPPER(COMERCIAL)
    def indiceBRUTO( self ) :
        self.setorder( 'BRUTO' ) # BRUTO
    def indiceCUENTA( self ) :
        self.setorder( 'CUENTA' ) # CUENTA

class RecibidasBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 14 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.CNUMERO = self.fieldget( 'CNUMERO' )
        obj.TIPONUM = self.fieldget( 'TIPONUM' ).rstrip()
        obj.CNUMALT = self.fieldget( 'CNUMALT' ).rstrip()
        obj.FECHA = self.fieldget( 'FECHA' )
        obj.REGFECHA = self.fieldget( 'REGFECHA' )
        obj.PROVEEDOR = self.fieldget( 'PROVEEDOR' )
        obj.PRCUENTA = self.fieldget( 'PRCUENTA' ).rstrip()
        obj.PRFACTURA = self.fieldget( 'PRFACTURA' ).rstrip()
        obj.PRFECHA = self.fieldget( 'PRFECHA' )
        obj.TIPOOP = self.fieldget( 'TIPOOP' )
        obj.TOCUENTA = self.fieldget( 'TOCUENTA' ).rstrip()
        obj.TOTAL = self.fieldget( 'TOTAL' )
        obj.TOTALDECL = self.fieldget( 'TOTALDECL' )
        obj.DECLTERC = self.fieldget( 'DECLTERC' ).rstrip()
        obj.ESTADO = self.fieldget( 'ESTADO' ).rstrip()
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        obj.REGISTRO = self.fieldget( 'REGISTRO' )
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceCNUMERO( self ) :
        self.setorder( 'CNUMERO' ) # STR(YEAR(FECHA),4)+TIPONUM+STR(CNUMERO,9)
    def indicePROVEEDOR( self ) :
        self.setorder( 'PROVEEDOR' ) # PROVEEDOR
    def indiceFECHA( self ) :
        self.setorder( 'FECHA' ) # DTOS(FECHA)+TIPONUM+STR(CNUMERO,9)
    def indiceREPETIDA( self ) :
        self.setorder( 'REPETIDA' ) # PRFACTURA+STR(PROVEEDOR,5)+DTOS(PRFECHA)

class RecibosBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 43 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.AGENTE = self.fieldget( 'AGENTE' )
        obj.TIPOAP = self.fieldget( 'TIPOAP' ).rstrip()
        obj.DIA = self.fieldget( 'DIA' )
        obj.MES = self.fieldget( 'MES' )
        obj.EJERCICIO = self.fieldget( 'EJERCICIO' )
        obj.IMPORTE = self.fieldget( 'IMPORTE' ).rstrip()
        obj.CONCEPTO = self.fieldget( 'CONCEPTO' ).rstrip()
        obj.RSEPARADO = self.fieldget( 'RSEPARADO' )
        obj.VTO = self.fieldget( 'VTO' ).rstrip()
        return obj

    def indiceAGENTE( self ) :
        self.setorder( 'AGENTE' ) # TIPO+STR(AGENTE,5)

class IVABase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 8 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        obj.IVA = self.fieldget( 'IVA' )
        obj.CTA_IVA = self.fieldget( 'CTA_IVA' ).rstrip()
        obj.IVA_RE = self.fieldget( 'IVA_RE' )
        obj.CTA_IVA_RE = self.fieldget( 'CTA_IVA_RE' ).rstrip()
        obj.PORDEFECTO = self.fieldget( 'PORDEFECTO' )
        obj.INACTIVO = self.fieldget( 'INACTIVO' )
        obj.ABREVIA = self.fieldget( 'ABREVIA' ).rstrip()
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # TIPO+STR(NUMERO,3)
    def indiceTEXTO( self ) :
        self.setorder( 'TEXTO' ) # TIPO+TEXTO

class OperacionesBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 10 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        obj.CUENTA = self.fieldget( 'CUENTA' ).rstrip()
        obj.PORDEFECTO = self.fieldget( 'PORDEFECTO' )
        obj.IVA = self.fieldget( 'IVA' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # TIPO+STR(NUMERO,3)
    def indiceTEXTO( self ) :
        self.setorder( 'TEXTO' ) # TIPO+TEXTO

class ReferenciasBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 15 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # TIPO+STR(NUMERO,3)
    def indiceTEXTO( self ) :
        self.setorder( 'TEXTO' ) # TIPO+TEXTO

class RefApuntesBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 16 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.TPNUMERO = self.fieldget( 'TPNUMERO' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # TIPO+STR(NUMERO,3)
    def indiceTPNUMERO( self ) :
        self.setorder( 'TPNUMERO' ) # TIPO+STR(TPNUMERO,8)

class TipoVtosBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 25 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        obj.CLIDEF = self.fieldget( 'CLIDEF' ).rstrip()
        obj.PROVDEF = self.fieldget( 'PROVDEF' ).rstrip()
        obj.ESTADO = self.fieldget( 'ESTADO' ).rstrip()
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO

class VencimientosBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 21 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.TPNUMERO = self.fieldget( 'TPNUMERO' )
        obj.FECHA = self.fieldget( 'FECHA' )
        obj.IMPORTE = self.fieldget( 'IMPORTE' )
        obj.PENDIENTE = self.fieldget( 'PENDIENTE' )
        obj.CUENTA = self.fieldget( 'CUENTA' ).rstrip()
        obj.CUENTADEF = self.fieldget( 'CUENTADEF' ).rstrip()
        obj.PENTIDAD = self.fieldget( 'PENTIDAD' )
        obj.PTIPO = self.fieldget( 'PTIPO' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceTIPO( self ) :
        self.setorder( 'TIPO' ) # TIPO+STR(TPNUMERO,8)
    def indicePENDIENTE( self ) :
        self.setorder( 'PENDIENTE' ) # PENDIENTE
    def indiceFECHA( self ) :
        self.setorder( 'FECHA' ) # DTOS(FECHA)

class ArticulosBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 28 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.CODIGO = self.fieldget( 'CODIGO' ).rstrip()
        obj.EAN13 = self.fieldget( 'EAN13' ).rstrip()
        obj.UBICACION = self.fieldget( 'UBICACION' ).rstrip()
        obj.PROVEEDOR = self.fieldget( 'PROVEEDOR' )
        obj.FAMILIA = self.fieldget( 'FAMILIA' )
        obj.NOMBRE = self.fieldget( 'NOMBRE' ).rstrip()
        obj.PVENTA = self.fieldget( 'PVENTA' )
        obj.DCTO = self.fieldget( 'DCTO' )
        obj.TDCTO = self.fieldget( 'TDCTO' ).rstrip()
        obj.DCTO2 = self.fieldget( 'DCTO2' )
        obj.DCTO3 = self.fieldget( 'DCTO3' )
        obj.PCOMPRA = self.fieldget( 'PCOMPRA' )
        obj.PCDCTO = self.fieldget( 'PCDCTO' )
        obj.PCDCTO2 = self.fieldget( 'PCDCTO2' )
        obj.PCDCTO3 = self.fieldget( 'PCDCTO3' )
        obj.TIPOIVAC = self.fieldget( 'TIPOIVAC' )
        obj.TIPOIVAV = self.fieldget( 'TIPOIVAV' )
        obj.OPERACIONC = self.fieldget( 'OPERACIONC' )
        obj.OPERACIONV = self.fieldget( 'OPERACIONV' )
        obj.ALBINVENT = self.fieldget( 'ALBINVENT' )
        obj.FINVENT = self.fieldget( 'FINVENT' )
        obj.QINVENT = self.fieldget( 'QINVENT' )
        obj.QCOMPRAS = self.fieldget( 'QCOMPRAS' )
        obj.QVENTAS = self.fieldget( 'QVENTAS' )
        obj.MINIMO = self.fieldget( 'MINIMO' )
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        obj.ASOCIADO = self.fieldget( 'ASOCIADO' )
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceNOMBRE( self ) :
        self.setorder( 'NOMBRE' ) # UPPER(NOMBRE)
    def indicePROVEEDOR( self ) :
        self.setorder( 'PROVEEDOR' ) # STR(PROVEEDOR,5)+NOMBRE
    def indiceCODIGO( self ) :
        self.setorder( 'CODIGO' ) # CODIGO
    def indiceEAN13( self ) :
        self.setorder( 'EAN13' ) # EAN13
    def indiceFAMILIA( self ) :
        self.setorder( 'FAMILIA' ) # FAMILIA

class ArticulosCBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 29 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.ARTICULO = self.fieldget( 'ARTICULO' )
        obj.CARNUM = self.fieldget( 'CARNUM' )
        obj.DATO = self.fieldget( 'DATO' ).rstrip()
        return obj

    def indiceARTICULO( self ) :
        self.setorder( 'ARTICULO' ) # ARTICULO

class FamiliasBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 37 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.PADRE = self.fieldget( 'PADRE' )
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        obj.DCTO = self.fieldget( 'DCTO' )
        obj.TDCTO = self.fieldget( 'TDCTO' ).rstrip()
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO

class FamiliasCBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 38 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.FAMILIA = self.fieldget( 'FAMILIA' )
        obj.CARNUM = self.fieldget( 'CARNUM' )
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        return obj

    def indiceFAMILIA( self ) :
        self.setorder( 'FAMILIA' ) # FAMILIA

class AlbEmiBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 30 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.CNUMERO = self.fieldget( 'CNUMERO' )
        obj.TIPONUM = self.fieldget( 'TIPONUM' ).rstrip()
        obj.CNUMALT = self.fieldget( 'CNUMALT' ).rstrip()
        obj.FECHA = self.fieldget( 'FECHA' )
        obj.CLIENTE = self.fieldget( 'CLIENTE' )
        obj.FACTURA = self.fieldget( 'FACTURA' )
        obj.IMPORTE = self.fieldget( 'IMPORTE' )
        obj.APUNTES = self.fieldget( 'APUNTES' )
        obj.CPI = self.fieldget( 'CPI' ).rstrip()
        obj.ORDEN = self.fieldget( 'ORDEN' )
        obj.ESTADOREP = self.fieldget( 'ESTADOREP' ).rstrip()
        obj.ESTADO = self.fieldget( 'ESTADO' ).rstrip()
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceCNUMERO( self ) :
        self.setorder( 'CNUMERO' ) # STR(YEAR(FECHA),4)+TIPONUM+STR(CNUMERO,9)
    def indiceCLIENTE( self ) :
        self.setorder( 'CLIENTE' ) # STR(CLIENTE,5)+DTOS(FECHA)
    def indiceFECHA( self ) :
        self.setorder( 'FECHA' ) # DTOS(FECHA)+TIPONUM+STR(CNUMERO,9)
    def indiceFACTURA( self ) :
        self.setorder( 'FACTURA' ) # FACTURA

class AlbRecBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 31 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.CNUMERO = self.fieldget( 'CNUMERO' )
        obj.TIPONUM = self.fieldget( 'TIPONUM' ).rstrip()
        obj.CNUMALT = self.fieldget( 'CNUMALT' ).rstrip()
        obj.FECHA = self.fieldget( 'FECHA' )
        obj.PROVEEDOR = self.fieldget( 'PROVEEDOR' )
        obj.FACTURA = self.fieldget( 'FACTURA' )
        obj.PRALBARAN = self.fieldget( 'PRALBARAN' ).rstrip()
        obj.PRFECHA = self.fieldget( 'PRFECHA' )
        obj.IMPORTE = self.fieldget( 'IMPORTE' )
        obj.APUNTES = self.fieldget( 'APUNTES' )
        obj.CPI = self.fieldget( 'CPI' ).rstrip()
        obj.ORDEN = self.fieldget( 'ORDEN' )
        obj.ESTADOREP = self.fieldget( 'ESTADOREP' ).rstrip()
        obj.PEDIDO = self.fieldget( 'PEDIDO' )
        obj.ESTADO = self.fieldget( 'ESTADO' ).rstrip()
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceCNUMERO( self ) :
        self.setorder( 'CNUMERO' ) # STR(YEAR(FECHA),4)+TIPONUM+STR(CNUMERO,9)
    def indicePROVEEDOR( self ) :
        self.setorder( 'PROVEEDOR' ) # STR(PROVEEDOR,5)+DTOS(FECHA)
    def indiceFECHA( self ) :
        self.setorder( 'FECHA' ) # DTOS(FECHA)+TIPONUM+STR(CNUMERO,9)
    def indiceFACTURA( self ) :
        self.setorder( 'FACTURA' ) # FACTURA
    def indiceREPETIDA( self ) :
        self.setorder( 'REPETIDA' ) # PRFACTURA+STR(PROVEEDOR,5)+DTOS(PRFECHA)

class AlbRepBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 32 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.ALBARAN = self.fieldget( 'ALBARAN' )
        obj.FACTURA = self.fieldget( 'FACTURA' )
        obj.IMPORTE = self.fieldget( 'IMPORTE' )
        obj.APUNTES = self.fieldget( 'APUNTES' )
        obj.CPI = self.fieldget( 'CPI' ).rstrip()
        obj.ORDEN = self.fieldget( 'ORDEN' )
        obj.REPARTO = self.fieldget( 'REPARTO' ).rstrip()
        return obj

    def indiceALBARAN( self ) :
        self.setorder( 'ALBARAN' ) # TIPO+STR(ALBARAN,8)
    def indiceFACTURA( self ) :
        self.setorder( 'FACTURA' ) # TIPO+STR(FACTURA,8)

class AlbPreBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 33 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.CNUMERO = self.fieldget( 'CNUMERO' )
        obj.TIPONUM = self.fieldget( 'TIPONUM' ).rstrip()
        obj.CNUMALT = self.fieldget( 'CNUMALT' ).rstrip()
        obj.FECHA = self.fieldget( 'FECHA' )
        obj.CLIENTE = self.fieldget( 'CLIENTE' )
        obj.IMPORTE = self.fieldget( 'IMPORTE' )
        obj.APUNTES = self.fieldget( 'APUNTES' )
        obj.ESTADO = self.fieldget( 'ESTADO' ).rstrip()
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceCNUMERO( self ) :
        self.setorder( 'CNUMERO' ) # STR(YEAR(FECHA),4)+TIPONUM+STR(CNUMERO,9)
    def indiceCLIENTE( self ) :
        self.setorder( 'CLIENTE' ) # STR(CLIENTE,5)+DTOS(FECHA)
    def indiceFECHA( self ) :
        self.setorder( 'FECHA' ) # DTOS(FECHA)+TIPONUM+STR(CNUMERO,9)

class AlbPedBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 40 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.CNUMERO = self.fieldget( 'CNUMERO' )
        obj.TIPONUM = self.fieldget( 'TIPONUM' ).rstrip()
        obj.CNUMALT = self.fieldget( 'CNUMALT' ).rstrip()
        obj.FECHA = self.fieldget( 'FECHA' )
        obj.PROVEEDOR = self.fieldget( 'PROVEEDOR' )
        obj.IMPORTE = self.fieldget( 'IMPORTE' )
        obj.APUNTES = self.fieldget( 'APUNTES' )
        obj.ESTADO = self.fieldget( 'ESTADO' ).rstrip()
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceCNUMERO( self ) :
        self.setorder( 'CNUMERO' ) # STR(YEAR(FECHA),4)+TIPONUM+STR(CNUMERO,9)
    def indicePROVEEDOR( self ) :
        self.setorder( 'PROVEEDOR' ) # STR(PROVEEDOR,5)+DTOS(FECHA)
    def indiceFECHA( self ) :
        self.setorder( 'FECHA' ) # DTOS(FECHA)+TIPONUM+STR(CNUMERO,9)

class AlbPedEBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 47 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.CNUMERO = self.fieldget( 'CNUMERO' )
        obj.TIPONUM = self.fieldget( 'TIPONUM' ).rstrip()
        obj.CNUMALT = self.fieldget( 'CNUMALT' ).rstrip()
        obj.FECHA = self.fieldget( 'FECHA' )
        obj.CLIENTE = self.fieldget( 'CLIENTE' )
        obj.IMPORTE = self.fieldget( 'IMPORTE' )
        obj.APUNTES = self.fieldget( 'APUNTES' )
        obj.ESTADO = self.fieldget( 'ESTADO' ).rstrip()
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceCNUMERO( self ) :
        self.setorder( 'CNUMERO' ) # STR(YEAR(FECHA),4)+TIPONUM+STR(CNUMERO,9)
    def indiceCLIENTE( self ) :
        self.setorder( 'CLIENTE' ) # STR(CLIENTE,5)+DTOS(FECHA)
    def indiceFECHA( self ) :
        self.setorder( 'FECHA' ) # DTOS(FECHA)+TIPONUM+STR(CNUMERO,9)

class AlbInvBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 34 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.NUMERO = self.fieldget( 'NUMERO' )
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.CNUMERO = self.fieldget( 'CNUMERO' )
        obj.TIPONUM = self.fieldget( 'TIPONUM' ).rstrip()
        obj.CNUMALT = self.fieldget( 'CNUMALT' ).rstrip()
        obj.FECHA = self.fieldget( 'FECHA' )
        obj.APUNTES = self.fieldget( 'APUNTES' )
        obj.MARCA = self.fieldget( 'MARCA' ).rstrip()
        obj.NOTAS = self.fieldget( 'NOTAS' )
        return obj

    def indiceNUMERO( self ) :
        self.setorder( 'NUMERO' ) # NUMERO
    def indiceCNUMERO( self ) :
        self.setorder( 'CNUMERO' ) # STR(YEAR(FECHA),4)+TIPONUM+STR(CNUMERO,9)
    def indiceFECHA( self ) :
        self.setorder( 'FECHA' ) # DTOS(FECHA)+STR(CNUMERO,9)

class ApuntesBase( DBFexten.DBFexten ) :
    def __init__( self ) :
        DBFexten.DBFexten.__init__( self, 35 )

    def regActual( self ) :
        obj = Anonimo()
        obj.recno = self.recno()
        obj.ALBARAN = self.fieldget( 'ALBARAN' )
        obj.TALBARAN = self.fieldget( 'TALBARAN' ).rstrip()
        obj.FECHA = self.fieldget( 'FECHA' )
        obj.TIPO = self.fieldget( 'TIPO' ).rstrip()
        obj.ARTICULO = self.fieldget( 'ARTICULO' )
        obj.TEXTO = self.fieldget( 'TEXTO' ).rstrip()
        obj.TEXTO2 = self.fieldget( 'TEXTO2' ).rstrip()
        obj.DCTO1 = self.fieldget( 'DCTO1' )
        obj.DCTO2 = self.fieldget( 'DCTO2' )
        obj.DCTO3 = self.fieldget( 'DCTO3' )
        obj.CANTIDAD = self.fieldget( 'CANTIDAD' )
        obj.PRECIO = self.fieldget( 'PRECIO' )
        obj.IMPORTE = self.fieldget( 'IMPORTE' )
        obj.TIVA = self.fieldget( 'TIVA' )
        obj.TIPOOP = self.fieldget( 'TIPOOP' )
        obj.CUENTA = self.fieldget( 'CUENTA' ).rstrip()
        obj.REPARTO = self.fieldget( 'REPARTO' ).rstrip()
        obj.GRUPO = self.fieldget( 'GRUPO' ).rstrip()
        obj.ALMACEN = self.fieldget( 'ALMACEN' ).rstrip()
        return obj

    def indiceALBARAN( self ) :
        self.setorder( 'ALBARAN' ) # TALBARAN+STR(ALBARAN,8)
    def indiceARTICULO( self ) :
        self.setorder( 'ARTICULO' ) # STR(ARTICULO,8)+DTOS(FECHA)
    def indiceFECHA( self ) :
        self.setorder( 'FECHA' ) # DTOS(FECHA)

