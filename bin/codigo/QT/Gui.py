# -*- coding: latin-1 -*-

#================================================================================================================================================

from PySide import QtCore, QtGui

#================================================================================================================================================

#================================================================================================================================================
def lanzaGUI( procesador, arg = None, estilo = "WindowsXP" ) :
    """
    Lanzador del interfaz gráfico de la aplicación.
    "WindowsXP", "Cleanlooks", "Plastique", "Windows", "Motif", "CDE"
    """
    app = QtGui.QApplication([])

    # Estilo
    styleName = estilo
    app.setStyle(QtGui.QStyleFactory.create(styleName))
    QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())

    # Lanzamos la pantalla
    procesador(arg)

    return app.exec_()
