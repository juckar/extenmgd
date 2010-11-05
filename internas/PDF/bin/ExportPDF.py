# -*- coding: latin-1 -*-

import sys

sys.path.append( gBase + "/library.zip" )

from reportlab.pdfgen import canvas
from reportlab.pdfbase import _fontdata

import ttf

# ###############################################################################################################
class PDF :
    def __init__( self, nomTXT, nomPDF ) :

        fichTXT = open( nomTXT )
        dmm = 72.0 / 2.54 * 0.01

        # Fuentes estandar
        self.FuentesStandar = [
                                ( "Courier", "Courier-Bold", "Courier-Oblique", "Courier-BoldOblique" ),
                                ( "Times-Roman", "Times-Bold", "Times-Italic", "Times-BoldItalic" ),
                                ( "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique" )
                            ]
        self.FS_Asociacion = [  (8,0), (10,0), (12,0),
                                (8,1), (10,1), (12,1), (14,1), (18,1), (24,1),
                                (8,2), (10,2), (12,2), (14,1), (18,1), (24,1),
                                (8,0)
                            ]
        # Fuentes True Type
        self.diccTTF = {}


        self.ALIN_IZQUIERDA = "2"

        # Leemos linea a linea el fichero de parámetros
        for linea in fichTXT :
            if len(linea) < 2 :
                continue

            # Eliminamos el retorno de carro
            linea = linea[:len(linea)-1]

            # Los parámetros vienen separados por ·
            self.op = linea.split( "·" )

            # El primer parámetro es la orden a realizar
            orden = self.op[0]


            if orden == "S" : # Parámetros generales
                self.ancho = float(self.op[1])*dmm
                self.alto = float(self.op[2])*dmm
                self.margenAncho = float(self.op[3])
                self.margenAlto = float(self.op[4])
                self.dirFonts = self.op[5]
                self.canvas = canvas.Canvas( nomPDF, pagesize=(self.ancho,self.alto), pageCompression = 0 )

            elif orden == "0" : # Mas parámetros
                self.filas = float(self.op[1])
                self.columnas = float(self.op[2])
                self.graficos = self.op[4].split( "|" )

            elif orden == "1" : # Texto
                self.PonTexto( )

            elif orden == "2" : # Imagen
                self.PonImagen(  )

            elif orden == "3" : # Lineas
                self.PonForma( )

            elif orden == "H" : # Fin de página
                self.canvas.showPage()

        # Cerramos el fichero de texto
        fichTXT.close()

        # Ponemos datos si los hay
        global Autor, Titulo, Asunto, PalClave
        if Autor :
            self.canvas.setAuthor( unicode( Autor, "latin-1" ) )
        if Titulo :
            self.canvas.setTitle( unicode( Titulo, "latin-1" ) )
        if Asunto :
            self.canvas.setSubject( unicode( Asunto, "latin-1" ) )
        if PalClave :
            self.canvas.setKeywords( unicode( PalClave, "latin-1" ) )

        # Grabamos el PDF
        self.canvas.save()

    # ###############################################################################################################
    # Ajustamos las coordenadas de MGD a reportlab
    def Y( self, fil ) :
        return (self.filas-fil)* self.alto/self.filas

    def X( self, col ) :
        return col * self.ancho/self.columnas
    # ###############################################################################################################
    # Calcula el ancho en puntos de un texto
    def AnchoTexto( self, cTexto, cFuente, nPuntos ) :
        return float(self.canvas.stringWidth( unicode( cTexto, "latin-1" ), cFuente, nPuntos ))

    # ###############################################################################################################
    # Tipo de letra
    def PonFuenteStandar( self, fuente, siNeg, siCur, siSub ) :
        tf = int(fuente)
        vf = self.FS_Asociacion[tf]
        puntos = vf[0]
        lf = self.FuentesStandar[vf[1]]
        nlf = 0
        if siNeg and siCur :
            nlf = 3
        elif siNeg :
            nlf = 1
        elif siCur :
            nlf = 2
        nombre = lf[nlf]
        self.canvas.setFont( nombre, puntos )
        return lf[nlf], puntos, _fontdata.ascent_descent[nombre]
    # ---------------------------------------------------------------------------------------------------------------
    def PonFuenteTTF( self, fuente, puntos, siNeg, siCur, siSub ) :
        if len(self.diccTTF) == 0 :
            self.diccTTF = ttf.ListaTTF( self.dirFonts )
        nomFuente, tAscentDescent = ttf.RegistraFuente( self.diccTTF, fuente, siNeg, siCur, siSub )
        self.canvas.setFont(nomFuente, puntos)
        return nomFuente, puntos, tAscentDescent

    # ---------------------------------------------------------------------------------------------------------------
    def PonFuente( self, c ) :
        opTMP = c.split( "|" )
        tipo = opTMP[0]
        fuente = opTMP[1]
        puntos = int(opTMP[2])
        siNeg = opTMP[3]=="S"
        siCur = opTMP[4]=="S"
        siSub = opTMP[5]=="S"
        if tipo == "N" :
            return self.PonFuenteStandar( fuente, siNeg, siCur, siSub )
        else :
            return self.PonFuenteTTF( fuente, puntos, siNeg, siCur, siSub )

    # ###############################################################################################################
    def PonColor( self, color ) :
        r = color % 256
        g = ((color - r )/256 ) % 256
        b = (((color - r )/256 - g) /256 ) % 256
        r = float(r)/256.0
        g = float(g)/256.0
        b = float(b)/256.0
        self.canvas.setFillColorRGB( r, g, b )
        self.canvas.setStrokeColorRGB( r, g, b )
    # ###############################################################################################################
    def PonTextoBloque( self, cTexto, nColumna, nFila, nAlineacion, nAncho, cFuente, nPuntos, tAscentDescent, nMaxFilas ) :
        lTexto = cTexto.split( "#-#*" )
        for unTexto in lTexto :
            nFilasUsadas = self.PonTextoFrase( unTexto, nColumna, nFila, nAlineacion, nAncho, cFuente, nPuntos, tAscentDescent, nMaxFilas )
            nMaxFilas -= nFilasUsadas
            if nMaxFilas <= 0 :
                return
            nFila -= (tAscentDescent[0]-tAscentDescent[1])*nPuntos/1000.00
    # ---------------------------------------------------------------------------------------------------------------
    def DivPalabras( self, cTexto ) :
        if len(cTexto) == 0 :
            return []
        nEspacios = 0
        for c in cTexto :
            if c != " " :
                break
            nEspacios += 1

        cTexto = cTexto[nEspacios:]
        lPalabras = cTexto.split( " " )
        if len(lPalabras) > 0 and nEspacios > 0 :
            lPalabras[0] = " "*nEspacios + lPalabras[0]
        return lPalabras

    # ---------------------------------------------------------------------------------------------------------------
    def PonTextoFrase( self, cTexto, nColumna, nFila, nAlineacion, nAncho, cFuente, nPuntos, tAscentDescent, nMaxFilas ) :

        lPalabras = self.DivPalabras( cTexto )
        nPalabras = len(lPalabras)
        if nPalabras < 1 :
            return 1

        cFrase = ""
        nFilasUsadas = 0
        for cPalabra in lPalabras :
            cNue = cFrase + cPalabra
            nTam = self.AnchoTexto( cNue, cFuente, nPuntos )
            if nTam > nAncho :
                self.PonTextoUno( cFrase, nColumna, nFila, nAlineacion, nAncho, cFuente, nPuntos, tAscentDescent )
                nFila -= (tAscentDescent[0]-tAscentDescent[1])*nPuntos/950.00
                cFrase = cPalabra + " "
                nFilasUsadas += 1
                if nMaxFilas <= nFilasUsadas :
                    break
            else :
                cFrase = cNue + " "
        if nMaxFilas > nFilasUsadas :
            if nAlineacion == "4" :
                nAlineacion = self.ALIN_IZQUIERDA
            self.PonTextoUno( cFrase, nColumna, nFila, nAlineacion, nAncho, cFuente, nPuntos, tAscentDescent )

        return nFilasUsadas
    # ---------------------------------------------------------------------------------------------------------------
    def PonTextoJustificado( self, cTexto, nColumna, nFila, nAncho, cFuente, nPuntos, tAscentDescent ) :
        nTamTexto = self.AnchoTexto( cTexto, cFuente, nPuntos )
        nPendiente = nAncho - nTamTexto
        if nPendiente == 0 :
            self.PonTextoUno( cTexto, nColumna, nFila, self.ALIN_IZQUIERDA, nAncho, cFuente, nPuntos, tAscentDescent )
            return

        if "...." in cTexto :
            nTamPunto = self.AnchoTexto( ".", cFuente, nPuntos )
            numPuntos = int(nPendiente/nTamPunto)
            if nPuntos :
                cTexto = cTexto.replace( "....", "."*(numPuntos+4), 1 )
                self.PonTextoUno( cTexto, nColumna, nFila, self.ALIN_IZQUIERDA, nAncho, cFuente, nPuntos, tAscentDescent )
                return

        cTexto = cTexto.rstrip()
        lPalabras = self.DivPalabras( cTexto )
        nPalabras = len(lPalabras)
        lTam = []
        nTamTexto = 0
        for i in range(nPalabras) :
            cPalabra = lPalabras[i]
            if i == nPalabras-1 :
                cPalabra += " "
            lTam.append( self.AnchoTexto( cPalabra, cFuente, nPuntos ) )
            nTamTexto += lTam[i]
        nPendiente = nAncho - nTamTexto

        if nPalabras > 1 :
            nPuntos = int(nPendiente/(nPalabras-1))
        else :
            nPuntos = 0
        nResto = nPendiente - nPuntos*nPalabras

        nPartida = nColumna
        for i in range(nPalabras) :
            self.PonTextoUno( lPalabras[i], nPartida, nFila, self.ALIN_IZQUIERDA, lTam[i], cFuente, nPuntos, tAscentDescent )
            nPartida += lTam[i] + nPuntos
            if i < nResto-1 :
                nPartida += 1

    # ---------------------------------------------------------------------------------------------------------------
    def PonTextoUno( self, cTexto, nColumna, nFila, nAlineacion, nAncho, cFuente, nPuntos, tAscentDescent ) :

        nMaxAlto = -tAscentDescent[1]*nPuntos/1000+nPuntos/9+1 #TTF
        nMaxAlto = 1.8 # std

        otro = unicode( cTexto, "latin-1" )
        n = len(otro)

        while self.canvas.stringWidth(otro, cFuente, nPuntos ) > nAncho :
            n -= 1
            otro = otro[:n]

        cBase = cTexto[:n]
        cTexto = cBase.decode('WinAnsiEncoding','ignore').encode('utf8')
        nFilaX = float(nFila) + float(nMaxAlto)
        if nAlineacion == "1" :
            self.canvas.drawRightString(nColumna+nAncho,nFilaX,cTexto)
        elif nAlineacion == "3" :
            nTam = self.canvas.stringWidth(otro, cFuente, nPuntos )
            self.canvas.drawString(nColumna+(nAncho-nTam)/2,nFilaX,cTexto)
        elif nAlineacion == "4" :
            self.PonTextoJustificado( cBase, nColumna, nFila, nAncho, cFuente, nPuntos, tAscentDescent )
        else :
            self.canvas.drawString(nColumna,nFilaX,cTexto)
    # ---------------------------------------------------------------------------------------------------------------
    def PonTexto( self ) :
        cTexto = self.op[1]
        nFila = self.Y(float(self.op[2]))
        nColumna = self.X(float(self.op[3]))
        nAncho = self.X(float(self.op[4]))
        nAlineacion = self.op[5]
        nMaxFilas = int(self.op[7])
        color = int(self.op[8])

        if color :
            self.PonColor( color )

        cFuente, nPuntos, tAscentDescent = self.PonFuente( self.op[6] )
        if nMaxFilas <= 1 :
            self.PonTextoUno( cTexto, nColumna, nFila, nAlineacion, nAncho, cFuente, nPuntos, tAscentDescent )
        else :
            self.PonTextoBloque( cTexto, nColumna, nFila, nAlineacion, nAncho, cFuente, nPuntos, tAscentDescent, nMaxFilas )

        if color :
            self.canvas.setFillColorRGB(0,0,0)
            self.canvas.setStrokeColorRGB(0,0,0)

    # ###############################################################################################################
    def PonForma( self ) :
        y1 = float(self.op[1])
        x1 = float(self.op[2])
        y2 = float(self.op[3])
        x2 = float(self.op[4])
        color = int(self.op[5])
        tipo = int(self.op[6])
        grosor = int(self.op[7])
        forma = int(self.op[8])

        self.canvas.setLineWidth( grosor/2.0 )

        if tipo == 0 :
            self.canvas.setDash( 1, 0 )
        elif tipo == 1 :
            self.canvas.setDash( 11, 3 )
        elif tipo == 2 :
            self.canvas.setDash( 1, 2 )
        elif tipo == 3 :
            self.canvas.setDash( [11,1,1,1], 0 )
        elif tipo == 4 :
            self.canvas.setDash( [11,1,1,2,1,1], 0 )

        if color :
            self.PonColor( color )

        if forma == 1 : # linea
            self.canvas.line( self.X(x1), self.Y(y1), self.X(x2), self.Y(y2) )
        elif forma == 5 : # círculo
            self.canvas.ellipse( self.X(x1), self.Y(y1), self.X(x2), self.Y(y2) )
        elif forma == 4 : # círculo sólido
            self.canvas.ellipse( self.X(x1), self.Y(y1), self.X(x2), self.Y(y2), fill=1 )
        else :
            x = self.X(x1)
            y = self.Y(y2)
            nAncho = self.X(x2) - x
            xalto = self.Y(y1)-y
            if forma == 2 : # caja
                self.canvas.rect( x, y, nAncho, xalto )
            elif forma == 6 : # caja redondeada
                self.canvas.roundRect( x, y, nAncho, xalto, radius=nAncho/20 )
            elif forma == 3 : # caja sólida
                self.canvas.rect( x, y, nAncho, xalto, fill=1 )
            elif forma == 7 : # caja sólida redondeada
                self.canvas.roundRect( x, y, nAncho, xalto, radius=nAncho/20, fill=1 )

        if color :
            self.canvas.setFillColorRGB(0,0,0)
            self.canvas.setStrokeColorRGB(0,0,0)

    # ###############################################################################################################
    def PonImagen( self ) :
        pos = int(self.op[1])
        y = self.Y(float(self.op[2]))
        x = self.X(float(self.op[3]))
        nAncho = self.X(float(self.op[4]))
        xalto = float(self.op[5])*self.alto/self.filas
        try :
            self.canvas.drawImage( self.graficos[pos-1], x, y, nAncho, xalto )
        except :
            pass

# ###############################################################################################################

if __name__ == '__main__':

    import os
    import sys
    from jFusion import *

    FC = FusionMGD.clave # Forma abreviada de llamada a la función, que nos proporciona los parámetros indicados en el programa

    nomTXT = FC( "FDATOS" )
    nomPDF = FC( "DESTINO" )
    global Autor, Titulo, Asunto, PalClave
    Autor = FC( "AUTOR" )
    Titulo = FC( "TITULO" )
    Asunto = FC( "ASUNTO" )
    PalClave = FC( "PALCLAVE" )

    siError = False
    if os.path.isfile( nomPDF ) :
        os.remove( nomPDF )
        if os.path.isfile( nomPDF ) :
            raw_input( "No se ha podido crear de nuevo el fichero PDF, probablemente porque está abierto con Acrobat Reader." )
            siError = True

    if not siError :
        PDF( nomTXT, nomPDF )

# ###############################################################################################################

