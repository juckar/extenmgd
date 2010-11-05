# -*- coding: latin-1 -*-

f = open( "municipios-calles.txt", "rb" )

d = {}
for l in f :
    x = l.split( ";" )
    c = x[1] if x[2] == "true" else x[4].strip()
    cp = x[3]
    d[cp] = c

f.close()

li = d.keys()
li.sort()
mi = "áéíóúÁÉÍÓÚñ"
my = "AEIOUAEIOUÑ"

o = open( "codpostales.dat", "wb" )
for k in li :
    v = d[k].upper()
    for c in mi :
        if c in v :
            v = v.replace( c, my[mi.index(c)] )

    o.write( k+"·"+v +"·\n")
o.close()
