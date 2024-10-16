# Add path to FreeCAD Python interface
# path to your FreeCAD.so or FreeCAD.dll file
import sys
FREECAD_ABS_PATH = 'C:/PROGRA~1/FreeCAD 0.21/bin'
sys.path.append(FREECAD_ABS_PATH)

import os
os.system('"''C:\\PROGRA~1\\FreeCAD 0.21\\bin\\FreeCAD.exe''"')

# import the FreeCAD Python interface
try:
    import FreeCAD
    print('The FreeCAD Python interface has been loaded')
except ValueError:
    print('FreeCAD library not found. Please check the FREECADPATH variable in the import script is correct')

try:
    import FreeCADGui
    FreeCADGui.showMainWindow()
    print('The FreeCAD Python interface (GUI) has been loaded')
except ValueError:
    print('FreeCAD (GUI) library not found. Please check the FREECADPATH variable in the import script is correct.')

print('ready')
