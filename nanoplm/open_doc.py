import os
import FreeCADGui

doc = FreeCAD.openDocument('C:/Users/Aleksander/Documents/GitHub/nanoPLM/nanoplm/static/SBHH.FCStd')
destination = os.path.join('C:/Users/Aleksander/Documents/GitHub/nanoPLM/nanoplm/static/projects/SBHH.DXF')

import TechDraw
TechDraw.writeDXFPage(FreeCAD.activeDocument().Page, u"C:/Users/Aleksander/Desktop/test.dxf")

#doc.save()
#FreeCAD.closeDocument(doc.Name)

#FreeCADGui.doCommand('exit()')