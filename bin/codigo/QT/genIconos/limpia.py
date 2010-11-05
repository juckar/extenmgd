# -*- coding: latin-1 -*-
import os

def leeTema( cTema ) :
    f = open( cTema, "rb" )
    d = { "nuvola":[], "silk":[], "gnome":[]}
    for linea in f :
        linea = linea.strip()
        if linea :
            li = linea.split(" ")
            if len(li) == 3 and li[1] in d :
                d[li[1]].append( li[2].lower() )

    f.close()

    for dd in d :
        li = os.listdir(dd)
        lidd = d[dd]
        for c in li :
            c = c.lower()
            if c not in lidd :
                os.remove( dd + "/" + c )

    return d
#~ d = leeTema( "Formatos.tema" )

def miraClaves( fich ) :
    f = open( fich, "rt" )
    src = f.read()
    f.close()
    import re
    x = re.compile( r"(Iconos\.*\(\b?\))" )
    li = x.findall( src )
    for n, x in enumerate(li) :
        a = x.split( '"' )
        li[n] = a[1], x
    return li

for f in os.listdir( "../../../Code/QT" ) :
    if f.lower().endswith( ".py" ) :
        q = open( "../../../Code/QT/"+f, "rt" )
        for linea in q :
            if "Iconos." in linea :
                txt = linea[linea.index("Iconos."):]
                txt = txt[:txt.index("(")]
                print txt
        q.close()
