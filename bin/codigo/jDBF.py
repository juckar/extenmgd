#-*- coding: latin-1 -*-

import struct
import sys
from jFechas import *

class clDBF :
    """
    Acceso simple a ficheros DBF, sólo para lectura.
    """
    def __init__( self, nomFichero ) :
        self.cFichero = nomFichero
        try:
            self.f = open(nomFichero, "rb")
        except:
            import ED
            ED.mensaje( "No se puede abrir el fichero de datos : %s"%self.cFichero )
            sys.exit(0)
        self._LeeCabecera()

    def _LeeCabecera( self ) :
        self.cabecera = self.f.read(32)  # Cabecera
        if not self.cabecera:
            raise "Error en %s"%self.cFichero, "Fichero vacio"
        if len(self.cabecera) != 32:
            raise "Error en %s"%self.cFichero, "No es un fichero DBF"
        self.numRegistros, self.tamCabecera, self.tamRegistro = struct.unpack('<xxxxLHH20x', self.cabecera)
        self.numCampos = (self.tamCabecera - 33) / 32

        self.f.seek( 0 )
        self.cabecera = self.f.read(self.tamCabecera)
        self.campos = []
        self.registro = {}
        for i in xrange(self.numCampos):
            start = 32 + i*32
            stop  = start + 32
            name, typ, size, deci = struct.unpack('<11sc4xBB14x', self.cabecera[start : stop])
            name = name.replace('\0', '')
            self.campos.append((name, typ, size, deci))
            self.registro[name]=""

    def goto( self, nReg ) :
        """
        Rellena el diccionario registro con los valores de campos del registro nReg
        """
        if nReg < 1 or nReg > self.numRegistros :
            raise "Error en %s"%self.cFichero, "Se intenta acceder a un numero de registro que no existe=%s(numRegs=%s)"%(nReg,self.numRegistros)
        self.f.seek(self.tamCabecera + (nReg-1)*self.tamRegistro)
        reg = self.f.read(self.tamRegistro)
        self.borrado = reg[0] != ' '
        offset = 1  # Empezamos por el segundo caracter el primero es el de borrado
        for i in range( self.numCampos ) :
            name   = self.campos[i][0]
            type   = self.campos[i][1]
            length = self.campos[i][2]
            field  = reg[offset : offset + length]
            offset = offset + length  # Siguiente posición
            if type == "C" :
                valor = field.strip()
            elif type == "L" :
                valor = field in [ "S", "s", "T", "t", "1", "V", "v" ]
            elif type == "D" :
                valor = DB2fecha( field )
            elif type == "N" :
                decim  = self.campos[i][3]
                field = field.strip()
                if field == "" :
                    field = "0"
                if decim == 0 :
                    valor = int(field)
                else :
                    valor = float( field )
            else :
                valor = None
            self.registro[name] = valor

    def cerrar( self ) :
        self.f.close()
