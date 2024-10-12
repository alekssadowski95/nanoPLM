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

def create_3d_preview(dir_path):
    doc = FreeCAD.open(dir_path)
    
    doc.save()
    FreeCAD.closeDocument(doc.Name)
    print('Created 3D preview')

def create_technical_drawing(dir_path):
    doc = FreeCAD.open(dir_path)
    
    doc.save()
    FreeCAD.closeDocument(doc.Name)
    print('Created technical drawing')

def create_manufacturing_file(dir_path):
    doc = FreeCAD.open(dir_path)
    
    doc.save()
    FreeCAD.closeDocument(doc.Name)
    print('Created manufacturing file')
