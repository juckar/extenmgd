# -*- coding: latin-1 -*-

def dicNumeros(  ) :
    numeros = """DEFINE DBFBancos := 1
DEFINE DBFClientes := 2
DEFINE DBFCuentas := 3
DEFINE DBFEmitidas := 4
DEFINE DBFExApuntes := 5
DEFINE DBFExPlantillas := 6
DEFINE DBFExtras := 7
DEFINE DBFIVA := 8
DEFINE DBFMovBancos := 9
DEFINE DBFOperaciones := 10
DEFINE DBFPagos := 11
DEFINE DBFParametros := 12
DEFINE DBFProveedores := 13
DEFINE DBFRecibidas := 14
DEFINE DBFReferencias := 15
DEFINE DBFRefApuntes := 16
DEFINE DBFDiario := 17
DEFINE DBFDiarioTxt := 18
DEFINE DBFInformes := 19
DEFINE DBFInfApun := 20
DEFINE DBFVencimientos := 21
DEFINE DBFERiva := 22
DEFINE DBFFormDoc := 23
DEFINE DBFFormHoja := 24
DEFINE DBFTipoVtos := 25
DEFINE DBFLBI := 26
DEFINE DBFAjustes := 27
DEFINE DBFArticulos := 28
DEFINE DBFArticulosC := 29
DEFINE DBFAlbEmi := 30
DEFINE DBFAlbRec := 31
DEFINE DBFAlbRep := 32
DEFINE DBFAlbPre := 33
DEFINE DBFAlbInv := 34
DEFINE DBFApuntes := 35
DEFINE DBFApuntesPre := 36
DEFINE DBFFamilias := 37
DEFINE DBFFamiliasC := 38
DEFINE DBFDirectos := 39
DEFINE DBFAlbPed := 40
DEFINE DBFEtiCod := 41
DEFINE DBFEtiDat := 42
DEFINE DBFRecibos := 43
DEFINE DBFFotos := 44
DEFINE DBFActividad := 45
DEFINE DBFAnalitica := 46
DEFINE DBFAlbPedE := 47"""

    d = {}
    for linea in numeros.split( "\n" ) :
        linea = linea.strip()
        li = linea.split( " := " )
        numero = int(li[1].strip())
        alias = li[0][10:].strip().upper()
        d[alias] = numero
    return d

class Campo :
    def __init__( self, dato ) :
        li = dato.split( "," )
        self.nombre = li[0].replace( '"', "" ).strip()
        self.tipo = li[1].replace( '"', "" ).strip()
        self.tam = int(li[2])
        self.dec = int(li[3])
class Indice :
    def __init__( self, dato ) :
        li = dato.split( "," )
        self.nombre = li[0].replace( '"', "" ).strip()
        self.expresion = ",".join( li[3:] ).replace( '[', "" ).replace( ']', "" ).strip()[:-1]
        

class DBF :
    def __init__( self, nombre ) :
        self.nombre = nombre
        self.alias = nombre
        self.campos = []
        self.indices = []
        self.numero = 0

def leeINI() :
    f = open( "c:/mgd/programa/ini30/_DBFs35r31.ini", "rt" )

    liDBF = []
    for x in f :
        x = x.strip().replace( " ", "" )
        if "//" in x :
            x = x[:x.find("//")].strip()
        if x :
            if x[0] == "[" :
                cl = x.replace( "[", "" ).replace("]","")
                dbf = DBF( cl )
                liDBF.append(dbf)
            elif "=" in x :
                li = x.split( "=" )
                clave = li[0]
                valor = li[1]
                if clave.lower() == "alias" :
                    dbf.alias = valor
                elif clave in [ "Campo", "Cuenta" ] :
                    if valor.startswith( "?" ) :
                        valor = valor[1:]
                    dbf.campos.append( Campo(valor) )
                elif clave == "Indice" :
                    dbf.indices.append( Indice(valor) )

    f.close()

    d = dicNumeros()

    for dbf in liDBF :
        if dbf.alias.lower() not in [ "empresas", "pargen", "repform" ] :
            dbf.numero = d[dbf.alias.upper()]

    return liDBF

