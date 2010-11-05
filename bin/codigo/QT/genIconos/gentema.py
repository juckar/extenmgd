import base64
import os.path

def funcionPNG( nomFuncion, nomDir, nomFichero ) :
    cFich = "%s/%s"%(nomDir,nomFichero)
    if not os.path.isfile( cFich ) :
        raw_input( "No existe " + cFich )
        return ""
    f = open( cFich, "rb" )
    o = f.read()
    f.close()
    x = base64.b64encode( o )
    n = len(x)
    k = int(n/80)
    t = "def pm%s() :\r\n"%nomFuncion
    t += '    return PM("""'
    for i in xrange(k) :
        t += x[i*80:i*80+80] + "\\\r\n"
    if k*80 != n :
        t+= x[k*80:n]
    t += '""")\r\n\r\n'
    t += "def %s() :\r\n"%nomFuncion
    t += '    return QtGui.QIcon( pm%s() )\r\n\r\n'%nomFuncion
    return t

def leeTema( cTema ) :
    f = open( cTema, "rb" )
    liImgs = f.read().splitlines()
    f.close()

    q = open( "../Iconos.py", "wb" )

    q.write( """\"\"\"Iconos y pixmap usados en el programa\"\"\"
import base64
from PySide import QtGui

def PM( txt64 ) :
    pm = QtGui.QPixmap()
    pm.loadFromData( base64.b64decode( txt64 ), "PNG" )
    return pm
""" )

    for x in liImgs :
        li = x.strip().split( " " )
        if len(li) == 3 :
            q.write( funcionPNG( li[0], li[1], li[2] ) )

    q.close()

leeTema( "Formatos.tema" )

