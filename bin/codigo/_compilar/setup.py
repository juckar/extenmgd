# -*- coding: latin-1 -*-
# Base = GUI2exe de Andrea Gavana

from distutils.core import setup
import py2exe
import glob
import os
import zlib
import shutil

siWindows = True
siQT = True

librerias = [ "Enlace", "Util", "ED" ]
if siQT :
    librerias.append( "QT" )

libreriasB = [ "reportlab/pdfgen", "reportlab/pdfbase" ]

directos = [ "dbAccess", "jDBF", "jFechas", "jFusion", "ttf", "VarExten" ] # necesario para compatibilizar con los informes + python


shutil.rmtree("build", ignore_errors=True)

class Target(object):
    """ A simple class that holds information on our executable file. """
    def __init__(self, **kw):
        """ Default class constructor. Update as you need. """
        self.__dict__.update(kw)

data_files = []

includes = ['shutil', 'Image', 'odbc', 'pyXLWriter', "pyExcelerator", "pickle", "csv", "urllib" ]
if siQT :
    #~ includes.extend( ['sip', 'PyQt4.QtCore', 'PyQt4.QtGui'] )
    includes.extend( [ 'PySide.QtCore', 'PySide.QtGui'] )

for libs in librerias :
    for f in os.listdir( libs ) :
        if f.endswith( ".py" ) and not f.startswith( "__in" ) :
            includes.append( libs + "." + f[:-3] )

for libs in libreriasB :
    for f in os.listdir( "c:/Python27/Lib/site-packages/" + libs ) :
        if f.endswith( ".py" ) and not f.startswith( "__in" ) :
            includes.append( libs.replace( "/", "." ) + "." + f[:-3] )

for modu in directos :
    includes.append( modu )

excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter']
packages = []
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll', 'MSVCP90.dll']
icon_resources = [(1,'_compilar/exten.ico')]
bitmap_resources = []
other_resources = []

GUI2Exe_Target_1 = Target(
    # what to build
    script = "exten.py",
    icon_resources = icon_resources,
    bitmap_resources = bitmap_resources,
    other_resources = other_resources,
    dest_base = "exten",
    version = "1.00",
    company_name = "Gestión MGD",
    copyright = "Licencia GPL",
    name = "Extensiones Gestión MGD"
    )
    
if siWindows :
    cons = []
    win = [GUI2Exe_Target_1]
else :
    cons = [GUI2Exe_Target_1]
    win = []
    

setup(

    data_files = data_files,

    options = {"py2exe": {"compressed": 0,
                          "optimize": 0,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          #~ "bundle_files": 3,
                          "dist_dir": "..",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              },

    console = cons,
    windows = win
    )


if __name__ == "__main__":
    setup()
