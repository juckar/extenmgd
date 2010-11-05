# -*- coding: latin-1 -*-
"""
Interfaz a los layouts de PySide
"""

from PySide import QtCore, QtGui

#================================================================================================================================================
class V(QtGui.QVBoxLayout):
    """
    Acomodaci�n en vertical.
    """

    #--------------------------------------------------------------------------
    def control( self, control ) :
        """
        A�ade un control.
        """
        self.addWidget( control )
        return self

    #--------------------------------------------------------------------------
    def otro( self, layout ) :
        """
        A�ade otro layout.
        """
        self.addLayout( layout )
        return self

    #--------------------------------------------------------------------------
    def espacio( self, espacio ) :
        """
        A�ade espacio fijo.
        """
        self.addSpacing( espacio )
        return self

    #--------------------------------------------------------------------------
    def margen( self, n ) :
        """
        Margen exterior.
        """
        self.setMargin( n )
        return self

    #--------------------------------------------------------------------------
    def relleno( self, factor ) :
        """
        A�ade espacio de relleno, que ocupa lo que puede seg�n un factor = stretch.
        """
        self.addStretch( factor )
        return self
#================================================================================================================================================

#================================================================================================================================================
class H(QtGui.QHBoxLayout):
    """
    Acomodaci�n en horizontal.
    """

    #--------------------------------------------------------------------------
    def control( self, control ) :
        """
        A�ade un control.
        """
        self.addWidget( control )
        return self

    #--------------------------------------------------------------------------
    def otro( self, layout ) :
        """
        A�ade otro layout.
        """
        self.addLayout( layout )
        return self

    #--------------------------------------------------------------------------
    def espacio( self, espacio ) :
        """
        A�ade espacio fijo.
        """
        self.addSpacing( espacio )
        return self

    #--------------------------------------------------------------------------
    def ponSeparacion( self, tam ) :
        """
        Separaci�n entre controles
        """
        self.setSpacing( tam )
        return self

    #--------------------------------------------------------------------------
    def margen( self, n ) :
        """
        Margen exterior.
        """
        self.setMargin( n )
        return self

    #--------------------------------------------------------------------------
    def relleno( self, factor ) :
        """
        A�ade espacio de relleno, que ocupa lo que puede seg�n un factor = stretch.
        """
        self.addStretch( factor )
        return self
#================================================================================================================================================

#================================================================================================================================================
class G(QtGui.QGridLayout):
    """
    Acomodaci�n en tabla.
    """

    dicAlineacion = { None:QtCore.Qt.AlignLeft, "d":QtCore.Qt.AlignRight, "c":QtCore.Qt.AlignCenter }

    #--------------------------------------------------------------------------
    def control( self, control, fila, columna, numFilas=1, numColumnas=1, alineacion = None ) :
        """
        A�ade un control.
        """
        self.addWidget( control, fila, columna, numFilas, numColumnas, self.dicAlineacion[alineacion] )
        return self

    #--------------------------------------------------------------------------
    def controld( self, control, fila, columna, numFilas=1, numColumnas=1 ) :
        """
        A�ade un control.
        """
        self.addWidget( control, fila, columna, numFilas, numColumnas, self.dicAlineacion["d"] )
        return self

    #--------------------------------------------------------------------------
    def controlc( self, control, fila, columna, numFilas=1, numColumnas=1 ) :
        """
        A�ade un control.
        """
        self.addWidget( control, fila, columna, numFilas, numColumnas, self.dicAlineacion["c"] )
        return self

    #--------------------------------------------------------------------------
    def otro( self, layout, fila, columna, numFilas=1, numColumnas=1, alineacion = None ) :
        """
        A�ade otro layout.
        """
        self.addLayout( layout, fila, columna, numFilas, numColumnas, self.dicAlineacion[alineacion] )
        return self

    #--------------------------------------------------------------------------
    def margen( self, n ) :
        """
        Margen exterior.
        """
        self.setMargin( n )
        return self

    #--------------------------------------------------------------------------
    def rellenoColumna( self, col, factor ) :
        """
        A�ade espacio de relleno, que ocupa lo que puede seg�n un factor = stretch.
        """
        self.setColumnStretch(col, factor)
        return self

#================================================================================================================================================
