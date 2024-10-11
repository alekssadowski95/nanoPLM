import json

from flask import render_template, url_for, redirect

from nanoplm import app
from .forms import NewProductForm
#from .models import Product
from .sample import products


@app.route('/')
def home():
    print(app.config)
    return render_template('home.html', products = products) 


@app.route('/getting-started')
def getting_started():
    return render_template('getting-started.html', title = "Schnellstart") 

@app.route('/create-product', methods=['GET', 'POST'])
def create_product():
    form = NewProductForm()
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
    return render_template('create-product.html', title = "Neues Produkt", form = form) 


@app.route('/product/<product_uuid>')
def read_product(product_uuid):
    target_product = {}
    for product in products:
        if product['uuid'] == product_uuid:
            target_product = product
    return render_template('read-product.html', title = target_product['name'], product = target_product) 

@app.route('/update-product/<product_uuid>', methods=['GET', 'POST'])
def update_product(product_uuid):
    target_product = {}
    for product in products:
        if product['uuid'] == product_uuid:
            target_product = product
    return render_template('update-product.html', title = target_product['name'], product = target_product) 

@app.route('/delete-product/<product_uuid>', methods=['GET', 'POST'])
def delete_product(product_uuid):
    return redirect(url_for('home'))