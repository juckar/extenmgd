# -*- coding: latin-1 -*-
"""
Se establecen las clases Columna y ListaColumnas, que controlan las columnas en las vistas de registros
"""

import copy

from PySide import QtCore, QtGui

# ##############################################################################################################
class Columna :
    """
    Definici�n de cada columna del grid.
    """
    def __init__( self, clave, cabecera, ancho=100, siCentrado = False, siDerecha = False, rgbTexto = None, rgbFondo = None, siOrden = True, estadoOrden = 0, edicion=None, siEditable = None, siMostrar = True, siChecked = False  ) :
        """

        @param clave: referencia de la columna.
        @param cabecera: texto mostrado en el grid como cabecera.
        @param ancho: anchura en pixels.
        @param siCentrado: alineaci�n
        @param siDerecha: alineaci�n, se ha diferenciado la alineaci�n, para que al definir
            columnas sea m�s f�cilmente visible el tipo de alineaci�n, cuando no es a la izquierda.
        @param rgbTexto: color del texto como un entero.
        @param rgbFondo: color de fondo.
        @param siOrden: si se puede ordenar por este campo
        @param estadoOrden: indica cual es el orden inicial de la columna  -1 Desc, 0 No, 1 Asc
        @param edicion: objeto delegate usado para la edici�n de los campos de esta columna
        @param siEditable: este par�metro se usa cuando aunque la columna tiene un delegate asociado para mostrarla, sin embargo no es editable.
        @param siMostrar: si se muestra o no.
        @param siChecked: si es un campo de chequeo.
        """

        self.clave = clave
        self.cabeceraDef = self.cabecera = cabecera
        self.anchoDef = self.ancho = ancho

        alineacion = "i"
        if siCentrado :
            alineacion = "c"
        if siDerecha :
            alineacion = "d"
        self.alineacionDef = self.alineacion = alineacion

        self.rgbTextoDef = self.rgbTexto = rgbTexto or -1
        self.rgbFondoDef = self.rgbFondo = rgbFondo or -1

        self.posicion = 0

        self.siOrden = siOrden
        self.estadoOrden = estadoOrden # -1 Desc, 0 No, 1 Asc

        self.edicion = edicion
        self.siEditable = False
        if self.edicion :
            self.siEditable = True
            if not siEditable is None :
                self.siEditable = siEditable

        self.siMostrarDef = self.siMostrar = siMostrar
        self.siChecked = siChecked

        # Por defecto no es una f�rmula
        self.siFormula = False
        self.formula = ""
        self.siFormExec = False

        self.ponQT()

    def ponQT( self ) :
        """
        Convierte las variables en variables utilizables directamente por las rutinas PySide, a efectos de rapidez.
        """
        self.qtAlineacion = self.QTalineacion(self.alineacion)
        self.qtColorTexto = self.QTcolorTexto(self.rgbTexto)
        self.qtColorFondo = self.QTcolorFondo(self.rgbFondo)

    def porDefecto( self ) :
        """
        Pone la configuraci�n de la columna en sus valores por defecto.
        """
        if not self.siFormula :
            self.cabecera = self.cabeceraDef
            self.alineacion = self.alineacionDef
            self.rgbTexto = self.rgbTextoDef
            self.rgbFondo = self.rgbFondoDef
            self.siMostrar = self.siMostrarDef

    def QTalineacion( self, alin ) :
        """
        Convierte un par�metro de alineaci�n para que sea usable por PySide
        """
        if alin == "c" :
            qtalin = QtCore.Qt.AlignCenter
        elif alin == "d" :
            qtalin = QtCore.Qt.AlignRight+QtCore.Qt.AlignVCenter
        else :
            qtalin = QtCore.Qt.AlignLeft+QtCore.Qt.AlignVCenter

        return QtCore.QVariant(qtalin)

    def QTcolorTexto( self, rgb ) :
        """
        Convierte un par�metro de color del texto para que sea usable por PySide
        """
        if rgb == -1 :
            return QtCore.QVariant()
        else :
            return QtCore.QVariant(QtGui.QColor(rgb))

    def QTcolorFondo( self, rgb ) :
        """
        Convierte un par�metro de color del fondo para que sea usable por PySide
        """
        if rgb == -1 :
            return QtCore.QVariant()
        else :
            return QtCore.QVariant(QtGui.QBrush(QtGui.QColor(rgb)))

    def ponFormula( self, formula ) :
        self.formula = formula.strip().replace( "�", "." )
        self.siFormExec = "\n" in self.formula
        if self.siFormExec :
            self.formula = self.formula.replace( "\r\n", "\n" )

    def guardarConf( self, dic ) :
        """
        Guarda los valores actuales de configuraci�n de la columna.

        @param dic: diccionario con los datos del m�dulo al que pertenece la columna.
        """

        def x( c, v ) :
            dic["%s.%s"%( self.clave, c )] = v

        x( "CABECERA", self.cabecera )
        x( "ANCHO", str(self.ancho) )
        x( "ALINEACION", self.alineacion )
        x( "RGBTEXTO", str(self.rgbTexto) )
        x( "RGBFONDO", str(self.rgbFondo) )
        x( "POSICION", str(self.posicion) )
        x( "SIMOSTRAR", "S" if self.siMostrar else "N" )
        x( "SIFORMULA", "S" if self.siFormula else "N" )

        if self.siFormula :
            if self.siFormExec :
                form = self.formula.replace( "\n", "�" )
                x( "FORMULA", form )
            else :
                x( "FORMULA", self.formula )

    def recuperarConf( self, dic ) :
        """
        Recupera los valores de configuraci�n de la columna.

        @param dic: diccionario con los datos del m�dulo al que pertenece la columna.
        """
        def x( varTxt, varInt, tipo = "t" ) :
            clave = "%s.%s"%( self.clave, varTxt )
            if clave in dic :
                v = dic[clave]
                if tipo == "n" :
                    v = int(v)
                elif tipo == "l" :
                    v = v == "S"
                setattr( self, varInt, v )

        x( "CABECERA", "cabecera"  )
        x( "ANCHO", "ancho", "n" )
        x( "ALINEACION", "alineacion" )
        x( "RGBTEXTO", "rgbTexto", "n" )
        x( "RGBFONDO", "rgbFondo", "n" )
        x( "POSICION", "posicion", "n" )
        x( "SIMOSTRAR", "siMostrar", "l" )
        x( "SIFORMULA", "siFormula", "l" )
        x( "FORMULA", "formula" )

        self.ponQT()

        if self.siFormula :
            if "�" in self.formula :
                self.formula = self.formula.replace( "�", "\n" )
            self.ponFormula( self.formula )

        return self

    def evalua( self, dicLocals, siError = False ) :
        """
        Hace el c�lculo cuando se trata de columnas calculadas.
        @param dicLocals: diccionario con las variables (+sus valores) utilizados en la f�rmula.
        @param siError: si devuelve un mensaje de error, utilizable en las comprobaciones.
        """
        try :
            if self.siFormExec :
                exec( self.formula, {}, dicLocals )
                if "resultado" in dicLocals :
                    resultado = str(dicLocals["resultado"])
                else :
                    if siError :
                        resultado = "Error, falta proporcionar la respuesta en la variable resultado"
            else :
                resultado = str(eval( self.formula,{}, dicLocals ))
        except :
            resultado = "Error" if siError else ""

        return resultado
# ##############################################################################################################

class ListaColumnas :
    """
    Almacena la configuraci�n de columnas como un bloque.
    """
    def __init__( self ) :
        self.liColumnas = []
        self.posCreacion = 0

    def nueva( self, clave, cabecera="", ancho=100, siCentrado = False, siDerecha = False, rgbTexto = None, rgbFondo = None, siOrden = True, estadoOrden = 0, edicion=None, siEditable = None, siMostrar = True, siChecked = False  ) :
        """
        Contiene los mismos par�metros que la Columna.

        @param clave: referencia de la columna.
        @param cabecera: texto mostrado en el grid como cabecera.
        @param ancho: anchura en pixels.
        @param siCentrado: alineaci�n
        @param siDerecha: alineaci�n, se ha diferenciado la alineaci�n, para que al definir
            columnas sea m�s f�cilmente visible el tipo de alineaci�n, cuando no es a la izquierda.
        @param rgbTexto: color del texto como un entero.
        @param rgbFondo: color de fondo.
        @param siOrden: si se puede ordenar por este campo
        @param estadoOrden: indica cual es el orden inicial de la columna  -1 Desc, 0 No, 1 Asc
        @param edicion: objeto delegate usado para la edici�n de los campos de esta columna
        @param siEditable: este par�metro se usa cuando aunque la columna tiene un delegate asociado para mostrarla, sin embargo no es editable.
        @param siMostrar: si se muestra o no.
        @param siChecked: si es un campo de chequeo.

        @return: la columna creada.
        """
        columna = Columna( clave, cabecera, ancho, siCentrado, siDerecha, rgbTexto, rgbFondo, siOrden, estadoOrden, edicion, siEditable, siMostrar, siChecked  )
        self.liColumnas.append( columna )
        self.posCreacion += 1
        columna.posCreacion = self.posCreacion
        return columna

    def columna( self, numCol ) :
        return self.liColumnas[numCol]

    def borrarColumna( self, numCol ) :
        del self.liColumnas[numCol]

    def numColumnas( self ) :
        return len(self.liColumnas)

    def resetEstadoOrden( self ) :
        for x in self.liColumnas :
            x.estadoOrden = 0

    def porDefecto( self ) :
        for x in self.liColumnas :
            x.porDefecto()

    def columnasMostrables( self ) :
        """
        Crea un nuevo objeto con s�lo las columnas mostrables.
        """
        cols = [ columna for columna in self.liColumnas if columna.siMostrar ]
        cols.sort( lambda x, y: cmp(x.posicion, y.posicion))
        oColumnasR = ListaColumnas()
        oColumnasR.liColumnas = cols
        return oColumnasR

    def copy( self ) :
        """
        Crea una copia de esta lista, con columnas copias de las existentes.
        """
        oColumnasCopy = ListaColumnas()
        cols = [ copy.copy(columna) for columna in self.liColumnas ]
        cols.sort( lambda x, y: cmp(x.posicion, y.posicion))
        oColumnasCopy.liColumnas = cols
        return oColumnasCopy

    def nuevaClave( self ) :
        """
        Crea una clave nueva de columna, en base a un modelo = CALC_<numero>
        """
        liActual = [ columna.clave for columna in self.liColumnas if columna.siFormula ]
        numero = 1
        while True :
            clave = "CALC_%d"%numero
            if clave not in liActual :
                return clave
            numero += 1
