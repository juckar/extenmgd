# -*- coding: latin-1 -*-

from PySide import QtCore, QtGui

import Colocacion


#================================================================================================================================================
class ED(QtGui.QLineEdit):
    """
    Control de entrada de texto en una línea.
    """

    #--------------------------------------------------------------------------
    def __init__(self, parent, texto = None ):
        """
        @param parent: ventana propietaria.
        @param texto: texto inicial.
        """
        if texto :
            QtGui.QLineEdit.__init__(self, texto, None)
        else :
            QtGui.QLineEdit.__init__(self, None)
        self.parent = parent

        self.siMayusculas = False

        self.menu = None

    def soloLectura( self, sino ) :
        self.setReadOnly( sino )
        return self

    def deshabilitado( self, sino ) :
        self.setDisabled( sino )
        return self

    def capturaIntro( self, rutina ) :
        self.parent.connect( self, QtCore.SIGNAL( " returnPressed ()" ), rutina )
        return self

    #--------------------------------------------------------------------------
    def ponTexto(self, texto) :
        """
        Pone el texto en el campo.
        """
        self.setText( texto )

    #--------------------------------------------------------------------------
    def texto(self) :
        """
        Recupera el texto del campo.
        """
        txt = str(self.text( ))
        return txt

    #--------------------------------------------------------------------------
    def alinCentrado( self ) :
        """
        Alinea al centro.
        """
        self.setAlignment( QtCore.Qt.AlignHCenter )
        return self

    #--------------------------------------------------------------------------
    def alinDerecha( self ) :
        """
        Alinea a la derecha.
        """
        self.setAlignment( QtCore.Qt.AlignRight )
        return self

    #--------------------------------------------------------------------------
    def anchoMinimo( self, tam ) :
        """
        Ancho mínimo del campo.
        """
        self.setMinimumWidth( tam )
        return self

    #--------------------------------------------------------------------------
    def caracteres( self, num ) :
        """
        Número máximo de caracteres.
        @param num: número de caracteres máximo que puede contener.
        """
        self.setMaxLength( num )
        self.numCaracteres = num
        return self

    #--------------------------------------------------------------------------
    def anchoFijo( self, tam ) :
        """
        Ancho fijo del campo.
        @param tam: tamaño en pixels.
        """
        self.setFixedWidth( tam )
        return self

    #--------------------------------------------------------------------------
    def controlrx( self, regexpr ) :
        rx = QtCore.QRegExp( regexpr )
        validator = QtGui.QRegExpValidator( rx, self )
        self.setValidator( validator )
        return self

    #--------------------------------------------------------------------------
    def ponFuente( self, f ) :
        self.setFont( f )
        return self

#================================================================================================================================================
def spinBoxLB( valor, desde, hasta, etiqueta = None, maxTam=None ) :
    ed = QtGui.QSpinBox()
    ed.setRange(desde, hasta)
    ed.setSingleStep(1)
    ed.setValue(int(valor))
    if maxTam :
        ed.setFixedWidth( maxTam )
    if etiqueta :
        label = LB( etiqueta + " :" )
        return ed, label
    else :
        return ed

#================================================================================================================================================
def comboBoxLB( liOpciones, valor, etiqueta=None ) :
    cb = QtGui.QComboBox(  )
    for n, tp in enumerate(liOpciones) :
        cb.addItem( tp[0], QtCore.QVariant(tp[1]) )
        if tp[1] == valor :
            cb.setCurrentIndex( n )
    if etiqueta :
        return cb, LB( etiqueta + " :"  )
    else :
        return cb

def respComboBox( cb ) :
    return str(cb.itemData(cb.currentIndex()).toString())

#================================================================================================================================================
def checkBoxLB( etiqueta, valor ) :
    cb = QtGui.QCheckBox( etiqueta )
    cb.setChecked( valor )
    return cb

#================================================================================================================================================
def creaTB( parent, liAcciones, siTexto = True, tamIcon=32 ) :

    tb = QtGui.QToolBar("BASICO", None)

    tb.setIconSize( QtCore.QSize( tamIcon, tamIcon ) )

    if siTexto :
        tb.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

    lista = []
    for datos in liAcciones :
        if datos :
            titulo, cIcono, clave = datos
            accion = QtGui.QAction( titulo, parent)
            accion.setIcon( eval( "Iconos.%s()"%cIcono) )
            accion.setIconText( titulo )
            parent.connect( accion, QtCore.SIGNAL("triggered()"), parent.procesarTB )
            accion.clave = clave
            lista.append( accion )
            tb.addAction( accion )
        else :
            tb.addSeparator(  )
    tb.liAcciones = lista
    return tb
# ------------------------------------------------------------------------------------------------------------
def accionTB( tb, clave, siHabilitar ) :
    for accion in tb.liAcciones :
        if accion.clave == clave :
            accion.setEnabled( siHabilitar )
            return
    return


# ------------------------------------------------------------------------------------------------------------
class LB(QtGui.QLabel):
    """
    Etiquetas de texto.
    """

    #--------------------------------------------------------------------------
    def __init__(self, texto = None):
        """
        @param texto: texto inicial.
        """
        if texto :
            QtGui.QLabel.__init__(self, texto)
        else :
            QtGui.QLabel.__init__(self)

        self.setOpenExternalLinks( True )

    #--------------------------------------------------------------------------
    def ponTexto(self, texto) :
        """
        Asigna un texto a la etiqueta.
        """
        self.setText( texto )

    #--------------------------------------------------------------------------
    def texto(self) :
        return str(self.text())

    #--------------------------------------------------------------------------
    def ponFuente(self, f) :
        self.setFont( f )
        return self

    #--------------------------------------------------------------------------
    def alinCentrado( self ) :
        """
        Alinea al centro.
        """
        self.setAlignment( QtCore.Qt.AlignCenter )
        return self

    #--------------------------------------------------------------------------
    def alinDerecha( self ) :
        """
        Alinea a la derecha.
        """
        self.setAlignment( QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter )
        return self

    #--------------------------------------------------------------------------
    def anchoFijo( self, tam ) :
        """
        Ancho fijo del campo.
        """
        self.setFixedWidth( tam )
        return self

    #--------------------------------------------------------------------------
    def anchoMinimo( self, tam ) :
        """
        Ancho mínimo del campo.
        """
        self.setMinimumWidth( tam )
        return self

    #--------------------------------------------------------------------------
    def altoFijo( self, tam ) :
        """
        Alto fijo del campo.
        """
        self.setFixedHeight( tam )
        return self

    #--------------------------------------------------------------------------
    def ponImagen( self, pm ) :
        self.setPixmap( pm )
        return self

    #--------------------------------------------------------------------------
    def ponFondo( self, color ) :
        return self.ponFondoN( color.name() )

    #--------------------------------------------------------------------------
    def ponFondoN( self, color ) :
        self.setStyleSheet("QWidget { background-color: %s }" % color)
        return self

    #--------------------------------------------------------------------------
    def ponColor( self, color ) :
        return self.ponColorN( color.name() )

    #--------------------------------------------------------------------------
    def ponColorN( self, color ) :
        self.setStyleSheet("QWidget { color: %s }" % color)
        return self

    #--------------------------------------------------------------------------
    def ponColorFondoN( self, color, fondo ) :
        self.setStyleSheet("QWidget { color: %s; background-color: %s}" % (color,fondo) )
        return self

    #--------------------------------------------------------------------------
    def ponWrap( self ) :
        self.setWordWrap(True)
        return self

# ------------------------------------------------------------------------------------------------------------
class PB(QtGui.QPushButton):
    """
    Botón.
    """

    #--------------------------------------------------------------------------
    def __init__(self, parent, texto, rutina = None, plano = True ):
        """
        @param parent: ventana propietaria, necesario para conectar una rutina.
        @param texto: etiqueta inicial.
        @param rutina: rutina a la que se conecta el botón.
        """
        QtGui.QPushButton.__init__(self, texto, None)
        self.wParent = parent
        self.setFlat( plano )
        if rutina :
            self.conectar( rutina )

    #--------------------------------------------------------------------------
    def ponIcono(self, icono, tamIcon = 16) :

        self.setIcon( icono )
        self.setIconSize( QtCore.QSize( tamIcon, tamIcon ) )
        return self
    #--------------------------------------------------------------------------
    def ponFuente(self, f) :
        self.setFont( f )
        return self
    #--------------------------------------------------------------------------
    def anchoFijo( self, tam ) :
        """
        Ancho fijo del campo.
        """
        self.setFixedWidth( tam )
        return self
    #--------------------------------------------------------------------------
    def altoFijo( self, tam ) :
        """
        Alto fijo del campo.
        """
        self.setFixedHeight( tam )
        return self
    #--------------------------------------------------------------------------
    def cuadrado( self, tam ) :
        self.setFixedSize( tam, tam )
        return self

    #--------------------------------------------------------------------------
    def anchoMinimo( self, tam ) :
        """
        Ancho mínimo del campo.
        """
        self.setMinimumWidth( tam )
        return self

    #--------------------------------------------------------------------------
    def conectar( self, rutina ) :
        """
        Se indica la rutina asociada cuando se presiona.
        """
        self.wParent.connect( self, QtCore.SIGNAL("clicked()"), rutina )
        return self

    #--------------------------------------------------------------------------
    def ponFondo( self, txtFondo ) :
        self.setStyleSheet("QWidget { background: %s }"%txtFondo)
        return self

    #--------------------------------------------------------------------------
    def ponFondoN( self, ncolor ) :
        self.setStyleSheet("QWidget { background-color: %d }" % ncolor)
        return self

    #--------------------------------------------------------------------------
    def ponPlano( self, siPlano ) :
        self.setFlat( siPlano )
        return self

    #--------------------------------------------------------------------------
    def ponToolTip( self, txt ) :
        self.setToolTip( txt )
        return self
    #--------------------------------------------------------------------------
    def ponTexto( self, txt ) :
        self.setText( txt )

# --------------------------------------------------------------------------------------------------------
class RB(QtGui.QRadioButton) :
    #--------------------------------------------------------------------------
    def __init__(self, wParent, texto, rutina = None ):
        QtGui.QRadioButton.__init__( self, texto )
        if rutina :
            wParent.connect( self, QtCore.SIGNAL("clicked()"), rutina )
    #--------------------------------------------------------------------------
    def activa(self, siActivar = True ) :
        self.setChecked( siActivar )
        return self

# ------------------------------------------------------------------------------------------------------------
class GB(QtGui.QGroupBox):

    #--------------------------------------------------------------------------
    def __init__(self, wParent, texto, layout ):
        QtGui.QGroupBox.__init__(self, texto)
        self.setLayout(layout)
        self.wParent = wParent

    #--------------------------------------------------------------------------
    def ponFuente(self, f) :
        self.setFont( f )
        return self

    #--------------------------------------------------------------------------
    def alinCentrado(self) :
        self.setAlignment( QtCore.Qt.AlignHCenter )
        return self

    #--------------------------------------------------------------------------
    def conectar( self, rutina ) :
        """
        Se indica la rutina asociada cuando se presiona.
        """
        self.setCheckable( True )
        self.setChecked( False )
        self.wParent.connect( self, QtCore.SIGNAL("clicked()"), rutina )
        return self

#================================================================================================================================================
class Fichas( QtGui.QTabWidget ) :
    def nueva( self, control, titulo ) :
        self.addTab(control, titulo)

#================================================================================================================================================
class EM(QtGui.QTextEdit):
    """
    Control de entrada de texto en varias líneas.
    """

    #--------------------------------------------------------------------------
    def __init__(self, parent, texto = None ):
        """
        @param texto: texto inicial.
        """
        if texto is None :
            QtGui.QTextEdit.__init__(self, parent)
        else :
            QtGui.QTextEdit.__init__(self, texto, parent)
        self.parent = parent

        self.menu = None # menú de contexto

    #--------------------------------------------------------------------------
    def ponHtml(self, texto) :
        """
        Pone el texto en el campo.
        """
        self.setHtml( texto )

    #--------------------------------------------------------------------------
    def insertarHtml(self, texto) :
        """
        Inserta un texto en la posición del cursor.
        """
        self.insertHtml( texto )

    #--------------------------------------------------------------------------
    def soloLectura(self) :
        self.setReadOnly( True )
        return self

    #--------------------------------------------------------------------------
    def texto(self) :
        """
        Recupera el texto del campo.
        """
        return str(self.toPlainText( ))

    #--------------------------------------------------------------------------
    def anchoMinimo( self, tam ) :
        """
        Ancho mínimo del campo.
        """
        self.setMinimumWidth( tam )
        return self

    #--------------------------------------------------------------------------
    def altoMinimo( self, tam ) :
        """
        Alto mínimo del campo.
        """
        self.setMinimumHeight( tam )
        return self

    #--------------------------------------------------------------------------
    def anchoFijo( self, tam ) :
        """
        Ancho fijo del campo.
        """
        self.setFixedWidth( tam )
        return self

    #--------------------------------------------------------------------------
    def ponFuente( self, f ) :
        self.setFont( f )
        return self

#================================================================================================================================================

#================================================================================================================================================
class LMenu(QtGui.QMenu) :
    #--------------------------------------------------------------------------
    def __init__( self, titulo = None, icono = None, siDeshabilitado = False, owner = None ) :
        QtGui.QMenu.__init__(self,owner)

        if titulo :
            self.setTitle( titulo )
        if icono :
            self.setIcon( icono )
        if siDeshabilitado :
            self.setDisabled( True )

    #--------------------------------------------------------------------------
    def ponFuente(self, f) :
        self.setFont( f )
        return self

    #--------------------------------------------------------------------------
    def opcion( self, clave, rotulo, icono = None, siDeshabilitado = False, tipoLetra = None ) :
        if icono :
            accion = QtGui.QAction( icono, rotulo, self )
        else :
            accion = QtGui.QAction( rotulo, self )
        accion.clave = clave
        if siDeshabilitado :
            accion.setDisabled( True )
        if tipoLetra :
            accion.setFont( tipoLetra )
        self.addAction( accion )
        return accion

    #--------------------------------------------------------------------------
    def submenu( self, rotulo, icono = None, siDeshabilitado = False ) :
        menu = LMenu( rotulo, icono, siDeshabilitado, owner = self )
        menu.setFont( self.font() )
        self.addMenu( menu )
        return menu

    #--------------------------------------------------------------------------
    def mousePressEvent( self, event ) :
        self.siIzq = event.button() == QtCore.Qt.LeftButton
        self.siDer = event.button() == QtCore.Qt.RightButton
        resp = QtGui.QMenu.mousePressEvent(self,event)
        return resp

    #--------------------------------------------------------------------------
    def separador( self ) :
        self.addSeparator( )

    #--------------------------------------------------------------------------
    def lanza( self ) :
        resp = self.exec_(QtGui.QCursor.pos())
        if resp :
            return resp.clave
        else :
            return None

#================================================================================================================================================

# ------------------------------------------------------------------------------------------------------------
class PBAR(QtGui.QProgressBar):
    """
    Barra de progreso.
    """

    #--------------------------------------------------------------------------
    def __init__(self, parent ):
        QtGui.QProgressBar.__init__(self, None)
        self.wParent = parent
        
    def ponValor( self, valor ) :
        self.setValue( valor )

    def ponRango( self, desde, hasta ) :
        self.setRange( desde, hasta )
        return self

    #--------------------------------------------------------------------------
    def anchoMinimo( self, tam ) :
        """
        Ancho mínimo del campo.
        """
        self.setMinimumWidth( tam )
        return self
