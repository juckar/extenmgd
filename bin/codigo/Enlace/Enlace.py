# -*- coding: latin-1 -*-

import os
from ctypes import *
import types
import datetime

#===================================================================================================================
global _dll, _dllDir, _siEnlaceDBF, _siEnlaceMGD
_dll = None
_dllDir = None
_siEnlaceDBF = False
_siEnlaceMGD = False
#===================================================================================================================



#===================================================================================================================
def ponDirEnlace( carpeta ) :
    global _dllDir
    _dllDir = carpeta
    

#===================================================================================================================
def abreDLL() :
    global _dll, _dllDir
    if _dll is None :
        trabajoDir = os.getcwd() 
        os.chdir( _dllDir )
        _dll = CDLL( "mgd.dll")
        os.chdir( trabajoDir )
    return _dll
    

#===================================================================================================================
def enlaceDBF(  ) :
    
    dll = abreDLL()
    global _siEnlaceDBF
    
    if not _siEnlaceDBF :
        _siEnlaceDBF = True
        
        dll.dbf_inicio.argtype = [c_char_p]

        dll.dbf_open.argtype = [c_char_p,c_int]
        dll.dbf_open.restype = c_int
        dll.dbf_close.argtype = [c_int]

        dll.dbf_orden.argtype = [c_int, c_char_p]
        dll.dbf_orden_1.argtype = [c_int, c_char_p, c_char_p]
        dll.dbf_orden_1R.argtype = [c_int, c_char_p, c_char_p]
        dll.dbf_orden_1R.restype = c_char_p
        dll.dbf_orden_2.argtype = [c_int, c_char_p, c_char_p, c_char_p]
        dll.dbf_orden_R.argtype = [c_int, c_char_p]
        dll.dbf_orden_R.restype = c_char_p
        
        dll.dbf_access.argtype = [c_int, c_char_p]
        dll.dbf_access.restype = c_char_p
        
        dll.dbf_marca.argtype = [c_int]
        dll.dbf_marca.restype = c_int
        dll.dbf_recupera.argtype = [c_int]

        dll.dbf_field.argtype = [c_int, c_int]
        dll.dbf_field.restype = c_char_p
        
        dll.dbf_new.argtype = [c_char_p]
        dll.dbf_new.restype = c_int
        dll.dbf_newCampo.argtype = [c_int, c_char_p, c_char_p, c_int, c_int]
        dll.dbf_newCrea.argtype = [c_int]
        dll.dbf_newCrea.restype = c_int

        dll.dbf_inicio( "init" )
    
    return dll
    

#===================================================================================================================
def enlaceMGD(  ) :
    
    dll = abreDLL()
    global _siEnlaceMGD
    
    if not _siEnlaceMGD :
        _siEnlaceMGD = True
    
        dll.xInicio.argtype = [c_char_p]
        dll.xUsaEmpresa.argtype = [c_char_p, c_int]
        dll.xCerrar.argtype = [c_char_p]

        dll.leeparametro.argtype = [c_char_p]
        dll.leeparametro.restype = c_char_p

        dll.cierraDBF.argtype = [c_int]

        dll.ordenDBF.argtype = [c_int, c_char_p]
        dll.ordenDBF_1.argtype = [c_int, c_char_p, c_char_p]
        dll.ordenDBF_1R.argtype = [c_int, c_char_p, c_char_p]
        dll.ordenDBF_1R.restype = c_char_p
        dll.ordenDBF_2.argtype = [c_int, c_char_p, c_char_p, c_char_p]
        dll.ordenDBF_R.argtype = [c_int, c_char_p]
        dll.ordenDBF_R.restype = c_char_p
        dll.accessDBF.argtype = [c_int, c_char_p]
        dll.accessDBF.restype = c_char_p
        dll.marcaDBF.argtype = [c_int]
        dll.marcaDBF.restype = c_int
        dll.recuperaDBF.argtype = [c_int]
        dll.contabilizaDBF.argtype = [c_int]
        dll.accessDBF.argtype = [c_int, c_char_p]
        dll.accessDBF.restype = c_char_p
        dll.ultimoDBF.argtype = [c_int]
        dll.ultimoDBF.restype = c_int
        dll.cnumeroDBF.argtype = [c_int, c_char_p, c_char_p, c_char_p]
        dll.cnumeroDBF.restype = c_char_p
        dll.recalculasaldos.argtype = [c_int]
        dll.recalculasaldos.restype = c_int

        dll.vencimientoCliente.argtype = [c_char_p, c_char_p]
        dll.vencimientoCliente.restype = c_char_p

        dll.vencimientoProveedor.argtype = [c_char_p, c_char_p]
        dll.vencimientoProveedor.restype = c_char_p

        dll.vencimientoAutomatico.argtype = [c_char_p, c_char_p]
        dll.vencimientoAutomatico.restype = c_char_p

        dll.xInicio( "-" )
    
    return dll



#===================================================================================================================
def convierteZ( valor ) :
    t = type( valor )
    tipo = ""
    if t == types.StringType :
        v = valor
        tipo = "C"
    elif t == types.BooleanType :
        v = "S" if valor else "N"
        tipo = "L"
    elif t == types.IntType :
        v = str(valor)
        tipo = "E"
    elif t == types.FloatType :
        v = str(valor)
        tipo = "F"
    else  :
        v = "%4d%02d%02d"%( valor.year, valor.month, valor.day )
        tipo = "D"
    return tipo + v


#===================================================================================================================
def Zconvierte( valor ) :
    tipo = valor[0]
    valor = valor[1:]

    if tipo == "C" :
        v = valor
    elif tipo == "L" :
        v = valor == "S"
    elif tipo == "F" :
        v = float(valor)
    elif tipo == "E" :
        v = int(valor)
    elif tipo == "D" :
        v = datetime.date( int(valor[:4]), int(valor[4:6]), int(valor[6:]) )
    return v

#===================================================================================================================
class Field :
    def __init__( self, nombre, tipo, ancho = 0, decimales = 0 ) :
        self.nombre = nombre
        self.tipo = tipo
        if ancho == 0 :
            ancho = { "D":8, "M":10, "L":1 }[tipo]
        self.ancho = ancho
        self.decimales = decimales
#===================================================================================================================
