# -*- coding: latin-1 -*-
#================================================================================================

import os

from PySide import QtCore, QtGui

import QT.Gui as Gui
import QT.QTUtil as QTUtil
import QT.Controles as Controles
import QT.Colocacion as Colocacion
import QT.Iconos as Iconos

import Util.Util as Util

#================================================================================================
class WDatos(QtGui.QDialog):

    #--------------------------------------------------------------------------------------------
    def __init__( self, procesador ) :
        super(WDatos, self).__init__()
        
        self.procesador = procesador
        

        self.setWindowTitle( "Importación de datos de CONTARAPID" )
        self.setWindowFlags( QtCore.Qt.Dialog | QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowIcon( Iconos.Aplicacion() )

        # Creamos los controles
        lbFichero = Controles.LB( "Fichero a importar : " )
        self.btFichero = Controles.PB( self, self.procesador.fichImportar, self.buscaFichero, plano = False ).anchoMinimo( 300 )
        
        self.btImportar = Controles.PB( self, "Importar", self.importar, plano = False ).anchoMinimo( 300 )
        
        self.lbImportando = Controles.LB( )
        self.pbar = Controles.PBAR( self ).anchoMinimo( 300 )
        
        # Layout
        layout = Colocacion.G().controld( lbFichero, 0, 0 ).control( self.btFichero, 0, 1 )
        layout.controlc( self.btImportar, 1, 0, 1, 2 )
        layout.controld( self.lbImportando, 2, 0 ).control( self.pbar, 2, 1 ).margen( 20 )
        self.setLayout( layout )
        
        self.miraBotonImportar()
            
        self.lbImportando.hide()
        self.pbar.hide()

    #--------------------------------------------------------------------------------------------
    def closeEvent(self, event): 
        self.procesador.cerrar()

    #--------------------------------------------------------------------------------------------
    def buscaFichero( self ) :
        if self.procesador.fichImportar :
            carpeta = os.path.split( self.procesador.fichImportar ) [0]
        else :
            carpeta = "c:/"
        resp = QTUtil.leeFichero( self, carpeta, "txt" )
        
        if resp :
            self.procesador.fichImportar = resp
            self.btFichero.ponTexto( self.procesador.fichImportar )
            self.miraBotonImportar()
            
    #--------------------------------------------------------------------------------------------
    def miraBotonImportar( self ) :
        self.btImportar.setVisible( (len(self.procesador.fichImportar)>0) and (Util.tamFichero( self.procesador.fichImportar ) > 0) )
        
    #--------------------------------------------------------------------------------------------
    def ponPBar( self, nRegs ) :
        self.btImportar.hide()
        self.pbar.ponRango( 1, nRegs )
        self.lbImportando.ponTexto( "Importando %d regs : "% nRegs )
        self.lbImportando.show()
        self.pbar.show()
        QTUtil.refreshGUI()

    #--------------------------------------------------------------------------------------------
    def ponPosicion( self, nPos ) :
        self.pbar.ponValor( nPos )
        

    #--------------------------------------------------------------------------------------------
    def importar( self ) :
        self.btImportar.hide()
        self.procesador.importar()

    #--------------------------------------------------------------------------------------------
    def ponError( self, mensaje ) :
        QTUtil.mensError( self, error )



#================================================================================================
