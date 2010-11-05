
del ..\..\*.dll
del ..\..\*.zip
del ..\..\*.pyd
del ..\..\*.exe
copy setup.py ..
cd ..
python setup.py py2exe 
del setup.py




