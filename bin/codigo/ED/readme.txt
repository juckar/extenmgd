EasyDialogs for Windows version 1.16.0

EasyDialogs for Windows is a ctypes based emulation of the EasyDialogs module
included in the Python distribution for Macintosh. It attempts to be as
compatible as possible. Code using the Macintosh EasyDialogs module can often
be run unchanged on Windows using this module. The module has been tested on
Python 2.3 running on Windows NT, 98, XP, and 2003. I would appreciate
feedback at jimmy@retzlaff.com about experience running this on other
versions of Windows (I attempted to avoid APIs that weren't available on
Windows 95 or Windows NT 4.0).

EasyDialogs is written in pure Python using Thomas Heller's ctypes module
(http://starship.python.net/crew/theller/ctypes/) to call Windows APIs
directly. No Python GUI toolkit is used. This means that relatively small
distributions can be made with py2exe (or its equivalents). A simple test of
all the dialogs in EasyDialogs bundled up using py2exe results in a
distribution that is about 1.25MB. Using py2exe in concert with NSIS as shown
at http://starship.python.net/crew/theller/moin.cgi/SingleFileExecutable
allows the same test to run as a single file executable that is just under
500KB.

Documentation for the Macintosh version can be found at:

http://www.python.org/doc/current/mac/module-EasyDialogs.html

That documentation is also included in the standard distributions of Python
for Windows and it can be used for this Windows version of EasyDialogs as
well. Known differences include:

AskFileForOpen
    typeList is used for the same purpose, but file type handling is different
    between Windows and Macintosh, so the form of this argument is different.
    In an attempt to remain as similar as possible, a list of extensions can
    be supplied (e.g., ['*', 'txt', 'bat']). A more complete form is also
    allowed: [('All Files (*.*)', '*.*'), ('C Files (*.c, *.h)', '*.c;*.h')].
    The first item in each tuple is the text description presented to the
    user. The second item in each tuple is a semi-colon separated list of
    standard Windows wildcard patterns that will match files described in the
    text description.

    The following parameters are ignored on Windows:
    clientName, dialogOptionFlags, eventProc, filterProc, multiple,
    popupExtension, preferenceKey, previewProc, version, wanted

AskFileForSave
    fileType is used for the same purpose, but file type handling is different
    between Windows and Macintosh, so the form of this argument is different.
    In an attempt to remain as similar as possible, an extension can
    be supplied (e.g., 'txt'). A more complete form is also allowed:
    ('Text Files (*.txt)', '*.txt'). The first item in the tuple is the text
    description presented to the user. The second item in the tuple is a
    standard Windows wildcard pattern that will match files described in the
    text description.

    The following parameters are ignored on Windows:
    clientName, dialogOptionFlags, eventProc, fileCreator, filterProc,
    multiple, popupExtension, preferenceKey, previewProc, version, wanted

AskFolder
    The following parameters are ignored on Windows:
    clientName, dialogOptionFlags, eventProc, filterProc,
    multiple, popupExtension, preferenceKey, version, wanted

Prerequisites
EasyDialogs for Windows requires a 32-bit version of Windows, Python 2.3, and
ctypes 0.6.3 or newer.

Example usage:
import EasyDialogs

EasyDialogs .Message("Testing EasyDialogs.") # displays a message box

filename = EasyDialogs.AskFileForOpen() # presents a standard file-open dialog

# display a progress bar
bar = EasyDialogs.ProgressBar(maxval=100)
for i in range(100):
    bar.inc()
del bar
