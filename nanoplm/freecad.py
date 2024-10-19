from nanoplm import FreeCAD


def set_product_data_in_spreadsheet(dir_path, product):
    doc = FreeCAD.open(dir_path)
    spreadsheet = doc.getObject('Spreadsheet')
    # second argument of .set must be str not int
    spreadsheet.set("name", str(product['name']))
    spreadsheet.set("description", str(product['description']))
    spreadsheet.set("type", str(product['type']))
    spreadsheet.set("stammblattbreite", str(product['stammblattbreite']))
    spreadsheet.set("plattensitzhoehe", str(product['plattensitzhoehe']))
    spreadsheet.set("plattensitzlaenge", str(product['plattensitzlaenge']))
    spreadsheet.set("plattensitzwinkel", str(product['plattensitzwinkel']))
    spreadsheet.set("schnittbreite", str(product['schnittbreite']))
    spreadsheet.set("aussendurchmesser", str(product['aussendurchmesser']))
    spreadsheet.set("bohrungsdurchmesser", str(product['bohrungsdurchmesser']))
    spreadsheet.set("zaehnezahl", str(product['zaehnezahl']))
    spreadsheet.recompute()
    doc.recompute()
    doc.save()
    FreeCAD.closeDocument(doc.Name)
    product["freecad_available"] = True
    print('Updated Spreadsheet')

def create_preview_3d(dir_path, product):
    import os
    from nanoplm import MODULE_DIR_PATH
    destination = os.path.join(MODULE_DIR_PATH, 'static', 'projects', str(product["uuid"]) + '.stl')
    doc = FreeCAD.open(dir_path)

    __objs__ = []
    __objs__.append(doc.getObject("Body"))
    import Mesh
    if hasattr(Mesh, "exportOptions"):
        options = Mesh.exportOptions(destination)
        Mesh.export(__objs__, destination, options)
    else:
        Mesh.export(__objs__, destination)

    del __objs__
    
    doc.save()
    FreeCAD.closeDocument(doc.Name)
    product["preview_available"] = True
    print('Created 3D preview')

def create_generic_3d(dir_path, product):
    import os
    from nanoplm import MODULE_DIR_PATH
    destination = os.path.join(MODULE_DIR_PATH, 'static', 'projects', str(product["uuid"]) + '.step')

    doc = FreeCAD.open(dir_path)

    __objs__ = []
    __objs__.append(doc.getObject("Body"))
    import Import
    if hasattr(Import, "exportOptions"):
        options = Import.exportOptions(destination)
        Import.export(__objs__, destination, options)
    else:
        Import.export(__objs__, destination)

    del __objs__
    
    doc.save()
    FreeCAD.closeDocument(doc.Name)
    product["generic_available"] = True
    print('Created generic 3D')

def create_technical_drawing(dir_path, product):
    import sys

    import FreeCADGui

    import os
    from nanoplm import MODULE_DIR_PATH
    
    doc = FreeCAD.openDocument(dir_path)

    destination = os.path.join(MODULE_DIR_PATH, 'static', 'projects', str(product["uuid"]) + '.PDF')
    __objs__ = []
    __objs__.append(doc.getObject("Page001"))

    if hasattr(FreeCADGui, "exportOptions"):
        options = FreeCADGui.exportOptions(destination)
        FreeCADGui.export(__objs__, destination, options)
    else:
        FreeCADGui.export(__objs__, destination)

    del __objs__

    doc.save()
    FreeCAD.closeDocument(doc.Name)

    FreeCADGui.getMainWindow().close()

    print('Created technical drawing')

def create_manufacturing_file(dir_path, product):
    doc = FreeCAD.open(dir_path)
    
    doc.save()
    FreeCAD.closeDocument(doc.Name)
    print('Created manufacturing file')
