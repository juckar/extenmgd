# -*- coding: latin-1 -*-

import DBFs

def w( q, texto, nt = 0 ) :
    q.write( "    "*nt + texto + "\r\n" )

def wt( q, texto ) :
    w( q, texto, 1 )

def wtt( q, texto ) :
    w( q, texto, 2 )

def wttt( q, texto ) :
    w( q, texto, 3 )

def wb( q ) :
    w( q, "" )

def hazDBF( q, dbf ) :
    w( q, "class %sBase( DBFexten.DBFexten ) :"%dbf.alias )
    wt( q, "def __init__( self ) :" )
    wtt( q, "DBFexten.DBFexten.__init__( self, %d )" % dbf.numero  )

    wb( q )

    wt( q, "def regActual( self ) :" )
    wtt( q, "obj = Anonimo()" )
    wtt( q, "obj.recno = self.recno()" )
    for campo in dbf.campos :
        cl = campo.nombre.lower()
        cu = campo.nombre.upper()
        if campo.tipo == "C" :
            wtt( q, "obj.%s = self.fieldget( '%s' ).rstrip()"%(cu,cu) )
        else :
            wtt( q, "obj.%s = self.fieldget( '%s' )"%(cu,cu) )
    wtt( q, "return obj" )

    wb( q )

    for indice in dbf.indices :
        wt( q, "def indice%s( self ) :"%indice.nombre.upper() )
        wtt( q, "self.setorder( '%s' ) # %s"%(indice.nombre.upper(), indice.expresion) )

    wb( q )


liDBFs = DBFs.leeINI()

q = open( "../DBFmgdGen.py", "wb" )

w( q, "# -*- coding: latin-1 -*-" )
wb( q )
w( q, "import DBFexten" )
wb( q )
w( q, "class Anonimo :" )
wt( q, "pass" )
wb( q )

for dbf in liDBFs :
    if dbf.numero > 0 :
        hazDBF( q, dbf )

q.close()

print "# -*- coding: latin-1 -*-"
print "import DBFmgdGen"
for dbf in liDBFs :
    if dbf.numero > 0 :
        print "class %s( DBFmgdGen.%sBase ) :"%(dbf.alias,dbf.alias)
        print "    pass"

print "-"*80
for dbf in liDBFs :
    if dbf.numero > 0 :
        print "        self.%s = DBFmgd.%s( self.lib )"%( dbf.alias.lower(), dbf.alias )

print "-"*80
for dbf in liDBFs :
    if dbf.numero > 0 :
        print "        self.%s.close()"%( dbf.alias.lower(), )
