# -*- coding: latin-1 -*-
"""
Interfaz a los layouts de PySide
"""

from PySide import QtCore, QtGui

#================================================================================================================================================
class V(QtGui.QVBoxLayout):
    """
    Acomodación en vertical.
    """

    #--------------------------------------------------------------------------
    def control( self, control ) :
        """
        Añade un control.
        """
        self.addWidget( control )
        return self

    #--------------------------------------------------------------------------
    def otro( self, layout ) :
        """
        Añade otro layout.
        """
        self.addLayout( layout )
        return self

    #--------------------------------------------------------------------------
    def espacio( self, espacio ) :
        """
        Añade espacio fijo.
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
        Añade espacio de relleno, que ocupa lo que puede según un factor = stretch.
        """
        self.addStretch( factor )
        return self
#================================================================================================================================================

#================================================================================================================================================
class H(QtGui.QHBoxLayout):
    """
    Acomodación en horizontal.
    """

    #--------------------------------------------------------------------------
    def control( self, control ) :
        """
        Añade un control.
        """
        self.addWidget( control )
        return self

    #--------------------------------------------------------------------------
    def otro( self, layout ) :
        """
        Añade otro layout.
        """
        self.addLayout( layout )
        return self

    #--------------------------------------------------------------------------
    def espacio( self, espacio ) :
        """
        Añade espacio fijo.
        """
        self.addSpacing( espacio )
        return self

    #--------------------------------------------------------------------------
    def ponSeparacion( self, tam ) :
        """
        Separación entre controles
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
        Añade espacio de relleno, que ocupa lo que puede según un factor = stretch.
        """
        self.addStretch( factor )
        return self
#================================================================================================================================================

#================================================================================================================================================
class G(QtGui.QGridLayout):
    """
    Acomodación en tabla.
    """

    dicAlineacion = { None:QtCore.Qt.AlignLeft, "d":QtCore.Qt.AlignRight, "c":QtCore.Qt.AlignCenter }

    #--------------------------------------------------------------------------
    def control( self, control, fila, columna, numFilas=1, numColumnas=1, alineacion = None ) :
        """
        Añade un control.
        """
        self.addWidget( control, fila, columna, numFilas, numColumnas, self.dicAlineacion[alineacion] )
        return self

    #--------------------------------------------------------------------------
    def controld( self, control, fila, columna, numFilas=1, numColumnas=1 ) :
        """
        Añade un control.
        """
        self.addWidget( control, fila, columna, numFilas, numColumnas, self.dicAlineacion["d"] )
        return self

    #--------------------------------------------------------------------------
    def controlc( self, control, fila, columna, numFilas=1, numColumnas=1 ) :
        """
        Añade un control.
        """
        self.addWidget( control, fila, columna, numFilas, numColumnas, self.dicAlineacion["c"] )
        return self

    #--------------------------------------------------------------------------
    def otro( self, layout, fila, columna, numFilas=1, numColumnas=1, alineacion = None ) :
        """
        Añade otro layout.
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
        Añade espacio de relleno, que ocupa lo que puede según un factor = stretch.
        """
        self.setColumnStretch(col, factor)
        return self

#================================================================================================================================================
