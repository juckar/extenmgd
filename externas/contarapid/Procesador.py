# -*- coding: latin-1 -*-
#================================================================================================
# Gestor de todos los eventos de la aplicación
#================================================================================================
import os

import Util.Util as Util
import Enlace.Empresa as Empresa

import Ventanas
import QT.Gui as Gui
import QT.QTUtil as QTUtil

import Recibidas
import Emitidas

#================================================================================================
class Procesador :
    
    crRECIBIDA_ESTANDAR = 0
    crRECIBIDA_ABONO = 1
    crRECIBIDA_RECTIFICATIVA = 2
    crRECIBIDA_BIEN_INV = 3
    crRECIBIDA_EXENTA_IVA = 4
    crRECIBIDA_IVA_NO_DEDUCIBLE = 5
    crRECIBIDA_IVA_PARCIAL_DEDUCIBLE = 6
    crRECIBIDA_INTRACOMUNITARIA = 7
    crRECIBIDA_INTRACOMUNITARIA_ABONO = 8
    crEMITIDA_ESTANDAR = 9
    crEMITIDA_ABONO = 10
    crEMITIDA_EXENTA_IVA = 11
    crEMITIDA_EXPORTACION = 12
    crEMITIDA_INTRACOMUNITARIA = 13
    crEMITIDA_INTRACOMUNITARIA_ABONO = 14

    #--------------------------------------------------------------------------------------------
    def __init__( self, config ) :
        self.config = config
        
        self.fichParam = os.path.join( config.dirModulo, "param.ini" )
        self.dicParam = Util.ini2dicSimple( self.fichParam )
        self.fichImportar = self.dicParam["FICHERO"] if "FICHERO" in self.dicParam else ""

        self.w = None
    
    #--------------------------------------------------------------------------------------------
    def cerrar( self ) :
        pass
            
    #--------------------------------------------------------------------------------------------
    def lanzaGUI( self ) :
        def ventana( procesador ) :
            self.w = Ventanas.WDatos( procesador )
            self.w.show()
        Gui.lanzaGUI( ventana, self, estilo = "Cleanlooks" )

    #--------------------------------------------------------------------------------------------
    def guardaParam( self ) :
        ficheroAntiguo = self.dicParam["FICHERO"] if "FICHERO" in self.dicParam else ""

        if ficheroAntiguo != self.fichImportar :
            self.dicParam["FICHERO"] = self.fichImportar
            Util.dic2iniSimple( self.fichParam, self.dicParam )

    #--------------------------------------------------------------------------------------------
    def leeRegistros( self ) :
        f = open( self.fichImportar, "rb" )
        liRegs = []
        liClaves = None
        si1 = True
        for n, linea in enumerate(f) :
            if si1 :
                liClaves = linea.split( "|" )
                si1 = False
            elif linea :
                li = linea.split( "|" )
                tipo = li[0]
                d = {}
                d["LINEA"] = n+1
                for n in range( len(li) ) :
                    d[liClaves[n]] = li[n].strip()
                if tipo in "01" :
                    liRegs.append( d )
                    liUltimo = []
                    d[ "MAS" ] = liUltimo
                elif tipo == "I" :
                    liUltimo.append( d )
        f.close()
        if (liClaves is None ) or (len(liClaves) < 49 ) or (len(liRegs) == 0) :
            self.w.ponError( "El fichero %s tiene un formato incorrecto"%self.fichImportar )
            return None
        
        return liRegs
        
    #--------------------------------------------------------------------------------------------
    def importar( self ) :
        
        # Guardamos el nombre del fichero para la siguiente vez
        self.guardaParam()
            
        # Leemos todos los registros
        liRegs = self.leeRegistros()
        if liRegs is None :
            return
        
        # Los procesamos
        #-# Abrimos el enlace con mgd
        empresa = Empresa.Empresa( self.config, "S" )
    
        #-# Miramos uno a uno todos los registros
        self.w.ponPBar( len(liRegs) )
        
        liError = []

        for n, uno in enumerate(liRegs) :
            
            self.w.ponPosicion( n+1 )
            
            tipo = uno["37_Factura_Tipo_CR_Expedidor"] + uno["38_Factura_Tipo_CR_Receptor"]
            tipo = int(tipo.replace( " ", "" ))
            
            error = ""
            if tipo in [ self.crRECIBIDA_ESTANDAR, self.crRECIBIDA_ABONO, self.crRECIBIDA_RECTIFICATIVA, self.crRECIBIDA_BIEN_INV, self.crRECIBIDA_EXENTA_IVA, \
                            self.crRECIBIDA_IVA_NO_DEDUCIBLE, self.crRECIBIDA_IVA_PARCIAL_DEDUCIBLE, self.crRECIBIDA_INTRACOMUNITARIA, self.crRECIBIDA_INTRACOMUNITARIA_ABONO ] :
                error = Recibidas.recibida( True, empresa, uno )
                
            elif tipo in [ self.crEMITIDA_ESTANDAR, self.crEMITIDA_ABONO, self.crEMITIDA_EXENTA_IVA, self.crEMITIDA_EXPORTACION, self.crEMITIDA_INTRACOMUNITARIA, \
                            self.crEMITIDA_INTRACOMUNITARIA_ABONO ] :
                error = Emitidas.emitida( True, empresa, uno )
                
            else :
                error = "Tipo de factura desconocido = %d"%tipo
            
            if error :
                liError.append( error )
                
        if liError :
            empresa.cerrar()
            nomf = os.path.join( self.config.dirModulo, "errores.txt" )
            f = open( nomf, "wb" )
            for linea in liError :
                f.write( linea )
            f.close()
            
            
            QTUtil.mensError( self.w, "Se suspende la importación, se ha producido error en %d facturas. Se intenta mostrar en el block de notas (fichero=%s)"%(len(liError), nomf) )
            self.w.accept()
            os.startfile( nomf )
            return
            
        emi = rec = 0
        for n, uno in enumerate(liRegs) :
            
            self.w.ponPosicion( n+1 )
            
            tipo = uno["37_Factura_Tipo_CR_Expedidor"] + uno["38_Factura_Tipo_CR_Receptor"]
            tipo = int(tipo.replace( " ", "" ))
            
            if tipo in [ self.crRECIBIDA_ESTANDAR, self.crRECIBIDA_ABONO, self.crRECIBIDA_RECTIFICATIVA, self.crRECIBIDA_BIEN_INV, self.crRECIBIDA_EXENTA_IVA, \
                            self.crRECIBIDA_IVA_NO_DEDUCIBLE, self.crRECIBIDA_IVA_PARCIAL_DEDUCIBLE, self.crRECIBIDA_INTRACOMUNITARIA, self.crRECIBIDA_INTRACOMUNITARIA_ABONO ] :
                        
                Recibidas.recibida( False, empresa, uno )
                rec += 1

            elif tipo in [ self.crEMITIDA_ESTANDAR, self.crEMITIDA_ABONO, self.crEMITIDA_EXENTA_IVA, self.crEMITIDA_EXPORTACION, self.crEMITIDA_INTRACOMUNITARIA, \
                            self.crEMITIDA_INTRACOMUNITARIA_ABONO ] :
                Emitidas.emitida( False, empresa, uno )
                emi += 1
                
        QTUtil.mensaje( self.w, "Importadas %d facturas, \n\trecibidas=%d, \n\temitidas=%d"%( rec+emi,rec,emi) )
        empresa.cerrar()
        self.w.accept()
            
        
        
        
        
        
        
#================================================================================================
    
