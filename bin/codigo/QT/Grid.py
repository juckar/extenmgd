# -*- coding: latin-1 -*-
"""
El grid es un TableView de PySide.

Realiza llamadas a rutinas de la ventana donde está ante determinados eventos, o en determinadas situaciones,
siempre que la rutina se haya definido en la ventana :

    - gridDobleClickCabecera : ante un doble click en la cabecera, normalmente se usa para la reordenación de la tabla por la columna pulsada.
    - gridTeclaPulsada : al pulsarse una tecla, llama a esta rutina, para que pueda usarse por ejemplo en búsquedas.
    - gridTeclaControl : al pulsarse una tecla de control, llama a esta rutina, para que pueda usarse por ejemplo en búsquedas.
    - gridDobleClick : en el caso de un doble click en un registro, se hace la llamad a esta rutina
    - gridBotonDerecho : si se ha pulsado el botón derecho del ratón.
    - gridPonValor : si hay un campo editable, la llamada se produce cuando se ha cambiado el valor tras la edición.

    - gridColorTexto : si está definida se la llama al mostrar el texto de un campo, para determinar el color del mismo.
    - gridColorFondo : si está definida se la llama al mostrar el texto de un campo, para determinar el color del fondo del mismo.

"""

from PySide import QtCore, QtGui

# ##############################################################################################################
class ControlGrid(QtCore.QAbstractTableModel):
    """
    Modelo de datos asociado al grid, y que realiza todo el trabajo asignado por PySide
    """
    def __init__(self, tableView, wParent, oColumnasR ):
        """
        @param tableView:
        @param oColumnasR: ListaColumnas con la configuración de todas las columnas visualizables.
        """
        QtCore.QAbstractTableModel.__init__(self, wParent)
        self.wParent = wParent
        self.siOrden = False
        self.hh = tableView.horizontalHeader()
        self.siColorTexto = hasattr( self.wParent, "gridColorTexto" )
        self.siColorFondo = hasattr( self.wParent, "gridColorFondo" )
        self.font = tableView.font()
        self.siBold = hasattr( self.wParent, "gridBold" )
        if self.siBold :
            self.bfont = QtGui.QFont( self.font )
            self.bfont.setWeight( 75 )

        self.oColumnasR = oColumnasR

    def rowCount(self, parent):
        """
        Llamada interna, solicitando el número de registros.
        """
        self.numDatos = self.wParent.gridNumDatos()
        return self.numDatos

    def refresh( self ) :
        """
        Si hay un cambio del número de registros, la llamada a esta rutina actualiza la visualización.
        """
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        ant_ndatos = self.numDatos
        nue_ndatos = self.wParent.gridNumDatos()
        if ant_ndatos != nue_ndatos :
            if ant_ndatos < nue_ndatos :
                self.insertRows( ant_ndatos, nue_ndatos-ant_ndatos )
            else :
                self.removeRows( nue_ndatos, ant_ndatos-nue_ndatos )

        ant_ncols = self.numCols
        nue_ncols = self.oColumnasR.numColumnas()
        if ant_ncols != nue_ncols :
            if ant_ncols < nue_ncols :
                self.insertColumns( 0, nue_ncols-ant_ncols )
            else :
                self.removeColumns( nue_ncols, ant_ncols-nue_ncols )

        self.emit(QtCore.SIGNAL("layoutChanged()"))

    def columnCount(self, parent):
        """
        Llamada interna, solicitando el número de columnas.
        """
        self.numCols = self.oColumnasR.numColumnas()
        return self.numCols

    def data(self, index, role):
        """
        Llamada interna, solicitando información que ha de tener/contener el campo actual.
        """
        if not index.isValid():
            return QtCore.QVariant()

        columna = self.oColumnasR.columna(index.column())

        if role == QtCore.Qt.TextAlignmentRole :
            return columna.qtAlineacion
        elif role == QtCore.Qt.BackgroundRole :
            if self.siColorFondo :
                resp = self.wParent.gridColorFondo( index.row(), columna )
                if resp :
                    return QtCore.QVariant(resp)
            return columna.qtColorFondo
        elif role == QtCore.Qt.TextColorRole :
            if self.siColorTexto :
                resp = self.wParent.gridColorTexto( index.row(), columna )
                if resp :
                    return QtCore.QVariant(resp)
            return columna.qtColorTexto
        elif self.siBold and role == QtCore.Qt.FontRole :
            if self.wParent.gridBold( index.row(), columna ) :
                return QtCore.QVariant(self.bfont)
            return QtCore.QVariant()

        if columna.siChecked :
            if role == QtCore.Qt.CheckStateRole :
                valor = self.wParent.gridDato( index.row(), columna )
                return QtCore.QVariant( QtCore.Qt.Checked if valor else QtCore.Qt.Unchecked )
        elif role == QtCore.Qt.DisplayRole :
            return QtCore.QVariant(self.wParent.gridDato( index.row(), columna ))

        return QtCore.QVariant()

    def flags(self, index):
        """
        Llamada interna, solicitando mas información sobre las carcaterísticas del campo actual.
        """
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled

        flag = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        columna = self.oColumnasR.columna(index.column())
        if columna.siEditable :
            flag |= QtCore.Qt.ItemIsEditable

        if columna.siChecked :
            flag |= QtCore.Qt.ItemIsUserCheckable
        return flag

    def setData( self, index, valor, role = QtCore.Qt.EditRole ) :
        """
        Tras producirse la edición de un campo en un registro se llama a esta rutina para cambiar el valor en el origen de los datos.
        Se lanza gridPonValor en la ventana propietaria.
        """
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.EditRole or role == QtCore.Qt.CheckStateRole :
            columna = self.oColumnasR.columna(index.column())
            nfila = index.row()
            self.wParent.gridPonValor( nfila, columna, valor )
            index2 = self.createIndex(nfila, 1)
            self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &,const QModelIndex &)'), index2, index2)

        return True

    def headerData(self, col, orientation, role):
        """
        Llamada interna, para determinar el texto de las cabeceras de las columnas.
        """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            columna = self.oColumnasR.columna(col)
            return QtCore.QVariant(columna.cabecera)
        return QtCore.QVariant()

# ##############################################################################################################

class Cabecera( QtGui.QHeaderView ) :
    """
    Se crea esta clase para poder implementar el doble click en la cabecera.
    """
    def __init__( self, tvParent ) :
        QtGui.QHeaderView.__init__( self, QtCore.Qt.Horizontal )
        self.setMovable( True )
        self.setClickable( True )
        self.tvParent = tvParent

    def mouseDoubleClickEvent( self, event ) :
        numColumna = self.logicalIndexAt( event.x(), event.y() )
        self.tvParent.dobleClickCabecera( numColumna )
        return QtGui.QHeaderView.mouseDoubleClickEvent(self, event)

# ##############################################################################################################
class Grid(QtGui.QTableView):
    """
    Implementa un TableView, en base a la configuración de una lista de columnas.
    """

    #--------------------------------------------------------------------------
    def __init__(self, wParent, oColumnas, dicVideo=None, altoFila = 20, siSelecFilas=False ):
        """
        @param wParent: ventana propietaria
        @param oColumnas: configuración de las columnas.
        @param altoFila: altura de todas las filas.
        """

        QtGui.QTableView.__init__( self )

        self.wParent = wParent

        self.oColumnas = oColumnas
        if dicVideo :
            self.recuperarVideo( dicVideo )
        self.oColumnasR = self.oColumnas.columnasMostrables() # Necesario tras recuperar video

        self.cg = ControlGrid( self, wParent, self.oColumnasR )

        self.setModel(self.cg)
        self.setShowGrid(True)

        self.setHorizontalHeader( Cabecera(self) )

        vh = self.verticalHeader()
        vh.setResizeMode( QtGui.QHeaderView.Fixed )
        vh.setDefaultSectionSize( altoFila )
        vh.setVisible(False)

        sel = QtGui.QAbstractItemView.SelectRows if siSelecFilas else QtGui.QAbstractItemView.SelectItems

        self.setSelectionBehavior(sel)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        self.ponAnchosColumnas() # es necesario llamarlo desde aquí

    def releerColumnas(self) :
        """
        Cuando se cambia la configuración de las columnas, se vuelven a releer y se indican al control de datos.
        """
        self.oColumnasR = self.oColumnas.columnasMostrables()
        self.cg.oColumnasR = self.oColumnasR
        self.cg.refresh()
        self.ponAnchosColumnas()

    def ponAnchosColumnas(self) :
        for numCol, columna in enumerate(self.oColumnasR.liColumnas) :
            self.setColumnWidth( numCol, columna.ancho )
            if columna.edicion and columna.siMostrar :
                self.setItemDelegateForColumn( numCol, columna.edicion )

    def keyPressEvent( self, event ) :
        """
        Se gestiona este evento, ante la posibilidad de que la ventana quiera controlar,
        cada tecla pulsada, llamando a la rutina correspondiente si existe (gridTeclaPulsada/gridTeclaControl)
        """
        resp = QtGui.QTableView.keyPressEvent( self, event )
        k = event.key()
        m = int(event.modifiers())
        siShift = (m & QtCore.Qt.ShiftModifier) > 0
        siControl = (m & QtCore.Qt.ControlModifier) > 0
        siAlt = (m & QtCore.Qt.AltModifier) > 0
        if hasattr( self.wParent, "gridTeclaPulsada" ) :
            if not (siControl or siAlt) and k < 256 :
                self.wParent.gridTeclaPulsada( event.text() )
        if hasattr( self.wParent, "gridTeclaControl" ) :
            self.wParent.gridTeclaControl( k, siShift, siControl, siAlt )
        return resp

    #--------------------------------------------------------------------------------------------------------------------------------
    def wheelEvent( self, event ) :
        if hasattr( self.wParent, "gridWheelEvent" ) :
            self.wParent.gridWheelEvent( self, event.delta() > 0 )

    #--------------------------------------------------------------------------------------------------------------------------------
    def mouseDoubleClickEvent( self, event ) :
        """
        Se gestiona este evento, ante la posibilidad de que la ventana quiera controlar,
        cada doble click, llamando a la rutina correspondiente si existe (gridDobleClick)
        con el número de fila y el objeto columna como argumentos
        """
        resp = QtGui.QTableView.mouseDoubleClickEvent(self, event)
        if hasattr( self.wParent, "gridDobleClick" ) and event.button() == 1:
            fil, columna = self.posActual()
            self.wParent.gridDobleClick( fil, columna )
        return resp

    def mousePressEvent(self, event):
        """
        Se gestiona este evento, ante la posibilidad de que la ventana quiera controlar,
        cada pulsación del botón derecho, llamando a la rutina correspondiente si existe (gridBotonDerecho)
        """
        resp = QtGui.QTableView.mousePressEvent(self, event)
        button = event.button()
        if button == 2:
            if hasattr( self.wParent, "gridBotonDerecho" ) :
                fil, col = self.posActual()
                self.wParent.gridBotonDerecho( fil, col )
        elif button == 1:
            if hasattr( self.wParent, "gridBotonIzquierdo" ) :
                fil, col = self.posActual()
                self.wParent.gridBotonIzquierdo( fil, col )

        return resp

    def dobleClickCabecera( self, numColumna ) :
        """
        Se gestiona este evento, ante la posibilidad de que la ventana quiera controlar,
        los doble clicks sobre la cabecera , normalmente para cambiar el orden de la columna,
        llamando a la rutina correspondiente si existe (gridDobleClickCabecera) y con el
        argumento del objeto columna
        """
        if hasattr( self.wParent, "gridDobleClickCabecera" ) :
            self.wParent.gridDobleClickCabecera( self.oColumnasR.columna( numColumna ) )

    #--------------------------------------------------------------------------
    def guardarVideo(self, dic):
        """
        Guarda en el diccionario de video la configuración actual de todas las columnas

        @param dic: diccionario de video donde se guarda la configuración de las columnas
        """
        liClaves = []
        for n, columna in enumerate(self.oColumnasR.liColumnas) :
            columna.ancho = self.columnWidth( n )
            columna.posicion = self.columnViewportPosition( n )
            columna.guardarConf( dic )
            liClaves.append( columna.clave )

        # Las que no se muestran
        for columna in self.oColumnas.liColumnas :
            if columna.clave not in liClaves :
                columna.guardarConf( dic )
    #--------------------------------------------------------------------------
    def recuperarVideo(self, dic):
        """
        Recupera del diccionario de video la configuración actual de todas las columnas
        """

        # Miramos en dic, si hay columnas calculadas y las añadimos
        liCalc = [ k.split(".")[0] for k in dic.keys() if k.startswith( "CALC_" ) ]
        if liCalc :
            s = set(liCalc)
            for clave in s :
                columna = self.oColumnas.nueva( clave, siOrden = False )

        # Leemos todas las columnas
        for columna in self.oColumnas.liColumnas :
            columna.recuperarConf( dic )

        self.oColumnas.liColumnas.sort( lambda x, y: cmp(x.posicion, y.posicion))

    #--------------------------------------------------------------------------
    def anchoColumnas(self):
        """
        Calcula el ancho que corresponde a todas las columnas mostradas.
        """
        ancho = 0
        for n, columna in enumerate(self.oColumnasR.liColumnas) :
            ancho += columna.ancho
        return ancho

    #--------------------------------------------------------------------------
    def recno( self ) :
        """
        Devuelve la fila actual.
        """
        n = self.currentIndex().row()
        nX = self.cg.numDatos -1
        return n if n <= nX else nX

    #--------------------------------------------------------------------------
    def goto( self, fila, col ) :
        """
        Se sitúa en una posición determinada.
        """
        elem = self.cg.createIndex( fila, col )
        self.setCurrentIndex( elem )

    #--------------------------------------------------------------------------
    def gotop( self ) :
        """
        Se sitúa al principio del grid.
        """
        if self.cg.numDatos > 0 :
            self.goto( 0, 0 )

    #--------------------------------------------------------------------------
    def gobottom( self, col = 0 ) :
        """
        Se sitúa en el último registro del frid.
        """
        if self.cg.numDatos > 0 :
            self.goto( self.cg.numDatos-1, col )

    #--------------------------------------------------------------------------
    def refresh( self ) :
        """
        Hace un refresco de la visualización del grid, ante algún cambio en el contenido.
        """
        self.cg.refresh()

    #--------------------------------------------------------------------------
    def posActual( self ) :
        """
        Devuelve la posición actual.

        @return: tupla con ( num fila, objeto columna )
        """
        columna = self.oColumnasR.columna(self.currentIndex().column())
        return (self.currentIndex().row(), columna)

    #--------------------------------------------------------------------------
    def posActualN( self ) :
        """
        Devuelve la posición actual.

        @return: tupla con ( num fila, num  columna )
        """
        return (self.currentIndex().row(), self.currentIndex().column())

# ##############################################################################################################
