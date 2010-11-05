# -*- coding: latin-1 -*-

import os
import gc

from PySide import QtCore, QtGui

import Colocacion

import Iconos

import Controles

# ------------------------------------------------------------------------------------------------------------
def leeFichero( owner, carpeta, extension ) :
    resp = QtGui.QFileDialog.getOpenFileName( owner, "Fichero", carpeta, "Fichero %s (*.%s)"%(extension,extension) )
    if resp :
        return resp[0]
    else :
        return None

# ------------------------------------------------------------------------------------------------------------
def beep() :
    QtGui.QApplication.beep()

# ------------------------------------------------------------------------------------------------------------
def refreshGUI( siMax = False ) :
    QtCore.QCoreApplication.processEvents()
    QtGui.QApplication.processEvents()
    if siMax :
        gc.collect()

# ------------------------------------------------------------------------------------------------------------
dAlineacion = { "i": QtCore.Qt.AlignLeft, "d":QtCore.Qt.AlignRight, "c":QtCore.Qt.AlignCenter }
def qtAlineacion( cAlin ) :
    if cAlin not in dAlineacion :
        cAlin = "i"
    return dAlineacion[cAlin]

# ------------------------------------------------------------------------------------------------------------
def qtFuente( tipoLetra ) :
    """
    Genera una fuente de un objeto bloqueTexto
    """
    f = QtGui.QFont()
    f.fromString(str(tipoLetra))
    return f

# ------------------------------------------------------------------------------------------------------------
def qtColor( nColor ) :
    """
    Genera un color a partir de un dato numérico
    """
    return QtGui.QColor(nColor)

# ------------------------------------------------------------------------------------------------------------
def qtColorRGB( r, g, b ) :
    """
    Genera un color a partir del rgb
    """
    return QtGui.QColor(r,g,b)

# ------------------------------------------------------------------------------------------------------------
def qtBrush( nColor ) :
    """
    Genera un brush a partir de un dato numérico
    """
    return QtGui.QBrush(qtColor(nColor))

# ------------------------------------------------------------------------------------------------------------
def centraWindow( window ) :
    screen = QtGui.QDesktopWidget().screenGeometry()
    size =  window.geometry()
    window.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
# ------------------------------------------------------------------------------------------------------------
def tamEscritorio( ) :
    screen = QtGui.QDesktopWidget().screenGeometry()
    return screen.width(), screen.height()
# ------------------------------------------------------------------------------------------------------------
def anchoEscritorio( ) :
    screen = QtGui.QDesktopWidget().screenGeometry()
    return screen.width()

# ------------------------------------------------------------------------------------------------------------
class MensEspera(QtGui.QDialog):

    def __init__(self, parent, mensaje, siCancelar = False ): #siCancelar
        super( MensEspera, self ).__init__(parent)

        self.setWindowFlags( QtCore.Qt.SplashScreen )
        self.setStyleSheet("QDialog, QLabel { background: #79b600 }")
        lbi = QtGui.QLabel( )
        lbi.setPixmap(Iconos.pmMensEspera())

        self.lb = lb = Controles.LB( resalta(mensaje) ).ponFuente( qtFuente( TabTipos.TipoLetra( puntos = 12 ) ) )

        if siCancelar :
            self.siCancelado = False
            self.btCancelar = Controles.PB( self, "Cancelar", rutina = self.cancelar, plano = False ).ponIcono( Iconos.TB_Cancelar()).anchoFijo(100)

        ly = Colocacion.G().control( lbi, 0, 0, 3, 1 ).control( lb, 1, 1 )
        if siCancelar :
            ly.controlc( self.btCancelar, 2,1 )

        ly.margen( 25 )
        self.setLayout(ly)
        self.teclaPulsada = None

    def cancelar( self ) :
        self.siCancelado = True

    def cancelado( self ) :
        refreshGUI()
        return self.siCancelado

    def activarCancelar( self, siActivar ) :
        self.btCancelar.setVisible( siActivar )
        refreshGUI()
        return self

    def keyPressEvent( self, event ) :
        QtGui.QDialog.keyPressEvent( self, event )
        self.teclaPulsada = event.key()

    def rotulo(self, nuevo ) :
        self.lb.ponTexto( resalta(nuevo) )
        refreshGUI()

    def muestra(self) :
        self.show()
        refreshGUI()
        return self

    def final( self ) :
        self.close()
        refreshGUI()

# ------------------------------------------------------------------------------------------------------------
class BarraProgreso( QtGui.QProgressDialog ) :
    #~ bp = QTUtil.BarraProgreso( self, "me", 5 ).mostrar()
    #~ n = 0
    #~ for n in range(5) :
        #~ print n
        #~ bp.pon( n )
        #~ time.sleep(1)
        #~ if bp.siCancelado() :
            #~ break
    #~ bp.cerrar()

    def __init__( self, owner, titulo, mensaje, total ) :
        QtGui.QProgressDialog.__init__( self, mensaje, "Cancelar", 0, total, owner)
        self.total = total
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowFlags( QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint )
        self.setWindowTitle( titulo )
        self.owner = owner

    def mostrar( self ) :
        self.show()
        return self

    def mostrarAD( self ) :
        self.move( self.owner.x()+self.owner.width()-self.width(), self.owner.y() )

        self.show()
        return self

    def cerrar( self ) :
        self.setValue(self.total)
        self.close()

    def mensaje( self, mens ) :
        self.setLabelText( mens )

    def siCancelado( self ) :
        return self.wasCanceled()

    def pon( self, valor ) :
        self.setValue( valor )

# ------------------------------------------------------------------------------------------------------------
def resalta( mens, tipo = 4 ) :
    return ("<h%d>%s</h%d>"%( tipo,mens,tipo)).replace( "\n", "<br>" )

# ------------------------------------------------------------------------------------------------------------
def mensaje( parent, mens, titulo = None, siResalta = True, siArribaDerecha = False ) :
    w = Mensaje( parent, mens, titulo, siResalta )
    if siArribaDerecha :
        w.show()
        w.move( parent.x()+parent.width()-w.width(), parent.y() )
    w.muestra()

# ------------------------------------------------------------------------------------------------------------
class Mensaje(QtGui.QDialog):

    def __init__(self, parent, mens, titulo = None, siResalta = True ) :
        super( Mensaje, self ).__init__(parent)

        if titulo is None :
            titulo = "Mensaje"
        if siResalta :
            mens = resalta(mens)

        self.setWindowTitle( titulo )
        self.setWindowFlags( QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint )
        #~ self.setStyleSheet("QDialog, QLabel { background: #79b600 }")

        lbi = QtGui.QLabel( )
        lbi.setPixmap(Iconos.pmTB_Informacion())

        lbm = Controles.LB( mens )
        bt = Controles.PB( self, "Seguir", rutina = self.accept, plano = False )

        ly = Colocacion.G().control( lbi, 0, 0 ).control( lbm, 0, 1 ).controld( bt, 1,1 )

        ly.margen( 10 )
        self.setLayout(ly)

    def muestra(self) :
        self.exec_()
        refreshGUI()

# ------------------------------------------------------------------------------------------------------------
def mensError( parent, mens) :
    QtGui.QMessageBox.warning( parent, "Error", resalta(mens) )
# ------------------------------------------------------------------------------------------------------------
def pregunta( parent, mens ) :
    return QtGui.QMessageBox.question( parent, "Pregunta", resalta(mens), "Sí", "No" ) == 0
# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
def creaTBAceptarCancelar( parent, siDefecto = False ) :
    liAcciones = [ ( "Aceptar", "TB_Aceptar", "aceptar" ),
                    None,
                    ( "Cancelar", "TB_Cancelar", "cancelar" ),
                    ]
    if siDefecto :
        liAcciones.append( ( "Defecto", "TB_Defecto", "defecto" ) )
    liAcciones.append( None )

    return Controles.creaTB( parent, liAcciones, True )

# ------------------------------------------------------------------------------------------------------------
class Proceso(QtCore.QProcess):

    def __init__( self, exe ) :
        QtCore.QProcess.__init__( self )
        self.setWorkingDirectory ( os.path.abspath(os.path.dirname(exe)) )
        self.start( exe, QtCore.QStringList() )

        self.waitForStarted()

    def escribeLinea( self, linea ) :
        self.writeData( linea + "\n" )

    def esperaRespuesta( self, segundos = None ) :
        if segundos :
            total = segundos*1000
            self.waitForReadyRead(total)

        else :
            self.waitForReadyRead()
        return str(self.readAllStandardOutput())

    def terminar( self ) :
        try :
            self.close()
        except :
            pass

# ------------------------------------------------------------------------------------------------------------
def salirAplicacion( id ) :
    QtGui.QApplication.exit(id)

# ------------------------------------------------------------------------------------------------------------
def salvaFichero( pantalla, titulo, carpeta, filtro, siConfirmarSobreescritura = True ) :
    opciones = 0 if siConfirmarSobreescritura else QtGui.QFileDialog.DontConfirmOverwrite
    return QtGui.QFileDialog.getSaveFileName( pantalla, titulo, carpeta, filtro, options = opciones )

# ------------------------------------------------------------------------------------------------------------
def ponPortapapeles( texto ) :
    cb = QtGui.QApplication.clipboard()
    cb.setText( texto )

# ------------------------------------------------------------------------------------------------------------
def traePortapapeles(  ) :
    cb = QtGui.QApplication.clipboard()
    texto = cb.text( )
    return str(texto) if texto else None

