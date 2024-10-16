import json

from flask import render_template, url_for, redirect

from nanoplm import app
from .forms import CreateProductForm
#from .models import Product
from .sample import products


@app.route('/')
def home():
    if app.config['FIRST_STARTUP'] == True:
        return redirect(url_for('welcome'))
    return render_template('home.html', products = reversed(products)) 

@app.route('/welcome')
def welcome():
    app.config['FIRST_STARTUP'] = False
    return render_template('welcome.html') 

@app.route('/getting-started')
def getting_started():
    return render_template('getting-started.html', title = "Schnellstart") 

@app.route('/create-product', methods=['GET', 'POST'])
def create_product():
    template_product = products[-1]
    form = CreateProductForm()
    if form.validate_on_submit():
        new_product = {}
        new_product['uuid'] = generate_product_uuid()
        new_product['name'] = form.name.data
        new_product['description'] = form.description.data
        new_product['type'] = form.type.data
        new_product['stammblattbreite'] = form.stammblattbreite.data
        new_product['plattensitzhoehe'] = form.plattensitzhoehe.data
        new_product['plattensitzlaenge'] = form.plattensitzlaenge.data
        new_product['plattensitzwinkel'] = form.plattensitzwinkel.data
        new_product['schnittbreite'] = form.schnittbreite.data
        new_product['aussendurchmesser'] = form.aussendurchmesser.data
        new_product['bohrungsdurchmesser'] = form.bohrungsdurchmesser.data
        new_product['zaehnezahl'] = form.zaehnezahl.data
        new_product['status'] = 'Entwurf'
        new_product['freecad_available'] = False
        new_product['generic_available'] = False
        new_product['preview_available'] = False
        new_product['techdraw_available'] = False
        new_product['mfg_available'] = False
        new_product['outdated_data'] = False
        products.append(new_product)
        return redirect(url_for('home'))
    return render_template('create-product.html', title = "Produkt erstellen", form = form, product = template_product) 

@app.route('/product/<product_uuid>')
def read_product(product_uuid):
    target_product = {}
    for product in products:
        if product['uuid'] == product_uuid:
            target_product = product
    return render_template('read-product.html', title = target_product['name'], product = target_product) 

@app.route('/update-product/<product_uuid>', methods=['GET', 'POST'])
def update_product(product_uuid):
    target_product = None
    for product in products:
        if product['uuid'] == product_uuid:
            target_product = product
    form = CreateProductForm()
    if form.validate_on_submit():
        target_product['name'] = form.name.data
        target_product['description'] = form.description.data
        target_product['type'] = form.type.data
        target_product['stammblattbreite'] = form.stammblattbreite.data
        target_product['plattensitzhoehe'] = form.plattensitzhoehe.data
        target_product['plattensitzlaenge'] = form.plattensitzlaenge.data
        target_product['plattensitzwinkel'] = form.plattensitzwinkel.data
        target_product['schnittbreite'] = form.schnittbreite.data
        target_product['aussendurchmesser'] = form.aussendurchmesser.data
        target_product['bohrungsdurchmesser'] = form.bohrungsdurchmesser.data
        target_product['zaehnezahl'] = form.zaehnezahl.data
        target_product['outdated_data'] = True
        return redirect(url_for('home'))
    return render_template('update-product.html', title = target_product['name'], form = form, product = target_product) 

@app.route('/delete-product/<product_uuid>')
def delete_product(product_uuid):
    for product in products:
        if product['uuid'] == product_uuid:
            products.remove(product)
    return redirect(url_for('home'))

@app.route('/release-product/<product_uuid>')
def release_product(product_uuid):
    for product in products:
        if product['uuid'] == product_uuid and product['status'] != 'Freigegeben':
            product['status'] = 'Freigegeben'
    return redirect(url_for('home'))

@app.route('/add-cad/<product_uuid>')
def add_cad(product_uuid):
    return redirect(url_for('home'))

@app.route('/run-freecad-wizard/<product_uuid>')
def run_freecad_wizard(product_uuid):
    from .freecad import set_product_data_in_spreadsheet, create_preview_3d, create_generic_3d, create_technical_drawing, create_manufacturing_file
    for product in products:
        if product['uuid'] == product_uuid:
            destination = copy_freecad_file(product['uuid'])
            set_product_data_in_spreadsheet(destination, product)
            create_preview_3d(destination, product)
            create_generic_3d(destination, product)
            create_technical_drawing(destination, product)
            create_manufacturing_file(destination, product)
            product['outdated_data'] = False
    return redirect(url_for('home'))

@app.route('/action-editor/<product_uuid>')
def action_editor(product_uuid):
    target_product = {}
    for product in products:
        if product['uuid'] == product_uuid:
            target_product = product
    return render_template('action-editor.html', title = target_product["name"] + "- Action Builder", product = target_product)

def download_file(uuid, purpose):
    if purpose == 'preview':
        pass
    elif purpose == 'generic':
        pass
    elif purpose == 'techdraw':
        pass
    elif purpose == 'mfg':
        pass
    else:
        print('Tried downloading file with unknown purpose.')
    
def copy_freecad_file(uuid):
    import shutil
    from nanoplm import MODULE_DIR_PATH
    import os
    # Source file path
    source = os.path.join(MODULE_DIR_PATH, 'static', 'SBHH.FCStd')
    # Destination file path
    destination = os.path.join(MODULE_DIR_PATH, 'static', 'projects', str(uuid) + '.FCStd')
    # Copy the file
    shutil.copy(source, destination)
    return destination

def generate_product_uuid():
    import uuid
    return str(uuid.uuid4())


    