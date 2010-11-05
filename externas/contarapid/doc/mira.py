
for tipo in range( 15 ) :
    t = str(tipo)
    f = open( "contarap.txt", "rb" )
    q = open( "contarap%d.txt"%tipo, "wb" )
    si1 = True
    for n,linea in enumerate(f) :
        li = linea.strip().split( "|" )
        if si1 :
            si1 = False
            li1 = li
        else :
            tp = li[37]+li[36]
            if int(tp) == tipo :
                q.write("%40s : %d\r\n"%("Linea", n+1) )
                for n,x in enumerate(li) :
                    q.write( "%40s : %s\r\n"%(li1[n], x) )
                q.write( "\r\n" )
                
    f.close()
    q.close()
