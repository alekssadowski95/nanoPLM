import json

from flask import render_template, url_for, redirect

from nanoplm import app
from .forms import CreateProductForm
#from .models import Product
from .sample import products


@app.route('/')
def home():
    return render_template('home.html', products = products) 

@app.route('/getting-started')
def getting_started():
    return render_template('getting-started.html', title = "Schnellstart") 

@app.route('/create-product', methods=['GET', 'POST'])
def create_product():
    template_product = products[-1]
    form = CreateProductForm()
    if form.validate_on_submit():
        tmp_product = {
            "uuid": "3159432b76b2b8cd",
            "name": "Sägeblatt",
            "description": "Sägeblatt für Harthölzer",
            "type": "SBHH",
            "stammblattbreite": 2.0,
            "plattensitzhoehe": 3.5,
            "plattensitzlaenge": 3.55,
            "plattensitzwinkel": 40.25,
            "schnittbreite": 3.2,
            "aussendurchmesser": 160.50,
            "bohrungsdurchmesser": 18.0,
            "zaehnezahl": 80,
            "status": "Entwurf"
        }
        products.append(tmp_product)
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
            create_preview_3d(destination)
            create_generic_3d(destination)
            create_technical_drawing(destination)
            create_manufacturing_file(destination)
    return redirect(url_for('home'))

def download_file(uuid, purpose):
    if purpose == 'preview':
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
    source = os.path.join(MODULE_DIR_PATH, 'static', 'saegeblatt.FCStd')
    # Destination file path
    destination = os.path.join(MODULE_DIR_PATH, 'static', 'projects', str(uuid) + '.FCStd')
    # Copy the file
    shutil.copy(source, destination)
    return destination


    