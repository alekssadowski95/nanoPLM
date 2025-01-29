import json

from flask import render_template, url_for, redirect, request

from nanoplm import app, db, Component, Instance, Client, File
from .forms import CreateComponentForm, CreateComponentInstanceForm, CreateClientForm, CreateFileForm
from .sample import products


@app.route('/welcome')
def welcome():
    app.config['NANOPLM_FIRST_STARTUP'] = False
    return render_template('welcome.html', NANOPLM_MODULE_FREECADCMD = app.config['NANOPLM_MODULE_FREECADCMD'], SELECTED_FREECAD_VERSION = app.config['SELECTED_FREECAD_VERSION']) 

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/search/<search_query>')
def search(search_query):
    return render_template('search.html') 

@app.route('/getting-started')
def getting_started():
    return render_template('getting-started.html', title = "Schnellstart") 

'''
CRUD for components
'''
@app.route('/all-components')
def all_components():
    components = Component.query.filter_by(is_active = True).limit(1000).all()
    return render_template('all-components.html', components = components, len = len) 

@app.route('/create-component', methods=['GET', 'POST'])
def create_component():
    form = CreateComponentForm()
    if form.validate_on_submit():
        components = Component.query.filter_by().all()
        component_numbers = [component.component_number for component in components]
        component_numbers_temp = []
        for component_number in component_numbers:
            if component_number.startswith(form.component_number.data):
                component_numbers_temp.append(component_number)
        component_numbers_temp_no = []
        for component_number in component_numbers_temp:
            component_numbers_temp_no.append(int(component_number.split(".")[-1]))

        minor_number = "." + "1"
        if len(component_numbers_temp_no) > 0:
            minor_number = "." + str(max(component_numbers_temp_no) + 1)

        new_component = Component(
            uuid = generate_uuid(), 
            name = form.name.data, 
            description = form.description.data,
            status = 'draft',
            component_number = form.component_number.data + minor_number
            )
        db.session.add(new_component)
        db.session.commit()
        return redirect(url_for('all_components'))
    return render_template('create-component.html', form = form) 

@app.route('/read-component/<component_uuid>')
def read_component(component_uuid):
    target_component = Component.query.filter_by(uuid = component_uuid).first()
    component_instances = Instance.query.filter_by(is_active = True, component = component_uuid).limit(1000).all()
    return render_template('read-component.html', component = target_component, component_instances = component_instances, len = len) 

@app.route('/update-component/<component_uuid>', methods=['GET', 'POST'])
def update_component(component_uuid):
    target_component = Component.query.filter_by(uuid = component_uuid).first()
    form = CreateComponentForm()
    if form.validate_on_submit():
        target_component.name = form.name.data
        target_component.description = form.description.data
        db.session.commit()
        return redirect(url_for('all_components'))
    return render_template('update-component.html', component = target_component, form = form) 

@app.route('/delete-component/<component_uuid>', methods=['GET', 'POST'])
def delete_component(component_uuid):
    target_component = Component.query.filter_by(uuid = component_uuid).first()
    target_component.is_active = False
    db.session.commit()
    return redirect(url_for('all_components'))

'''
CRUD for component instances
'''
@app.route('/all-component-instances')
def all_component_instances():
    component_instances = Instance.query.filter_by(is_active = True).limit(1000).all()
    return render_template('all-component-instances.html', component_instances = component_instances, len = len) 

@app.route('/create-component-instance', methods=['GET', 'POST'])
def create_component_instance():
    target_component_uuid = request.args.get('component_uuid')
    target_client_uuid = request.args.get('client_uuid')

    form = CreateComponentInstanceForm()

    if target_component_uuid != None:
        target_component = Component.query.filter_by(uuid = target_component_uuid).first()
        form.component_uuid.choices = [(target_component.uuid, target_component.name)]
    else:
        components = Component.query.filter_by(is_active = True).limit(1000).all()
        form.component_uuid.choices = [(component.uuid, component.name) for component in components]
    
    if target_client_uuid != None:
        target_client = Client.query.filter_by(uuid = target_client_uuid).first()
        form.client_uuid.choices = [(target_client.uuid, target_client.name)]
    else:
        clients = Client.query.filter_by(is_active = True).limit(1000).all()
        form.client_uuid.choices = [(client.uuid, client.name) for client in clients]

    if form.validate_on_submit():
        new_component_instance = Instance(
            uuid = generate_uuid(), 
            serial_number = "1000001",
            component = form.component_uuid.data,
            client = form.client_uuid.data
            )
        db.session.add(new_component_instance)
        db.session.commit()
        return redirect(url_for('all_component_instances'))
    return render_template('create-component-instance.html', form = form) 

@app.route('/component-instance/<component_instance_uuid>')
def read_component_instance(component_instance_uuid):
    target_component_instance = Instance.query.filter_by(uuid = component_instance_uuid).first()
    return render_template('read-component-instance.html', component_instance = target_component_instance, len = len) 

"""
Updating Instances does not make sense. So will not be used
"""
@app.route('/update-component-instance/<component_instance_uuid>', methods=['GET', 'POST'])
def update_component_instance(component_instance_uuid):
    target_component_instance = Instance.query.filter_by(uuid = component_instance_uuid).first()
    form = CreateComponentInstanceForm()
    if form.validate_on_submit():
        target_component_instance.component = form.component.data
        target_component_instance.client = form.client.data
        db.session.commit()
        return redirect(url_for('all_component_instances'))
    return render_template('update-component-instance.html', form = form, component_instance = target_component_instance)

@app.route('/delete-component-instance/<component_instance_uuid>', methods=['GET', 'POST'])
def delete_component_instance(component_instance_uuid):
    target_component_instance = Instance.query.filter_by(uuid = component_instance_uuid).first()
    target_component_instance.is_active = False
    db.session.commit()
    return redirect(url_for('all_component_instances'))

'''
CRUD for clients
'''
@app.route('/all-clients')
def all_clients():
    clients = Client.query.filter_by(is_active = True).limit(1000).all()
    return render_template('all-clients.html', clients = clients, len = len) 

@app.route('/create-client', methods=['GET', 'POST'])
def create_client():
    form = CreateClientForm()
    if form.validate_on_submit():
        new_client = Client(
            uuid = generate_uuid(), 
            name = form.name.data
            )
        db.session.add(new_client)
        db.session.commit()
        return redirect(url_for('all_clients'))
    return render_template('create-client.html', form = form) 

@app.route('/read-client/<client_uuid>')
def read_client(client_uuid):
    target_client = Client.query.filter_by(uuid = client_uuid).first()
    component_instances = Instance.query.filter_by(is_active = True, client = client_uuid).limit(1000).all()
    return render_template('read-client.html', client = target_client, component_instances = component_instances, len = len) 

@app.route('/update-client/<client_uuid>', methods=['GET', 'POST'])
def update_client(client_uuid):
    target_client = Client.query.filter_by(uuid = client_uuid).first()
    form = CreateClientForm()
    if form.validate_on_submit():
        target_client.name = form.name.data
        db.session.commit()
        return redirect(url_for('all_clients'))
    return render_template('update-client.html', form = form, client = target_client)

@app.route('/delete-client/<client_uuid>', methods=['GET', 'POST'])
def delete_client(client_uuid):
    target_client = Client.query.filter_by(uuid = client_uuid).first()
    target_client.is_active = False
    db.session.commit()
    return redirect(url_for('all_clients'))

'''
CRUD for files
'''
@app.route('/all-files')
def all_files():
    files = File.query.filter_by(is_active = True).limit(1000).all()
    return render_template('all-files.html', files = files, len = len) 

@app.route('/create-file', methods=['GET', 'POST'])
def create_file():
    form = CreateFileForm()
    if form.validate_on_submit():
        new_file = File(
            uuid = generate_uuid(), 
            name = form.name.data
            )
        db.session.add(new_file)
        db.session.commit()
        return redirect(url_for('all_files'))
    return render_template('create-file.html', form = form) 

@app.route('/read-file/<file_uuid>')
def read_file(file_uuid):
    target_file = File.query.filter_by(uuid = file_uuid).first()
    return render_template('read-file.html', file = target_file) 

@app.route('/update-file/<file_uuid>', methods=['GET', 'POST'])
def update_file(file_uuid):
    target_file = File.query.filter_by(uuid = file_uuid).first()
    form = CreateFileForm()
    if form.validate_on_submit():
        target_file.name = form.name.data
        db.session.commit()
        return redirect(url_for('all_files'))
    return render_template('update-file.html', form = form, file = target_file) 

@app.route('/delete-file/<file_uuid>', methods=['GET', 'POST'])
def delete_file(file_uuid):
    target_file = File.query.filter_by(uuid = file_uuid).first()
    target_file.is_active = False
    db.session.commit()
    return redirect(url_for('all_files'))

'''
Module help
'''
@app.route('/module-info/<module_name>')
def module_help(module_name):
    if module_name == "item_engineeringtool":
        return render_template('item-engineeringtool-help.html') 
    if module_name == "all_components":
        return render_template('all-components-help.html') 
    if module_name == "3d_find_it":
            return render_template('3dfindit-help.html') 
    else:
        pass 

'''
Old stuff
'''
from .forms import CreateProductForm


@app.route('/all-products')
def all_products():
    return render_template('all-products.html', convert_to_five_digit_string = convert_to_five_digit_string, products = reversed(products), NANOPLM_MODULE_FREECADCMD = app.config['NANOPLM_MODULE_FREECADCMD'], SELECTED_FREECAD_VERSION = app.config['SELECTED_FREECAD_VERSION']) 

@app.route('/create-product', methods=['GET', 'POST'])
def create_product():
    template_product = products[-1]
    form = CreateProductForm()
    if form.validate_on_submit():
        new_product = {}
        new_product['uuid'] = generate_uuid()
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
    return render_template('read-product.html', convert_to_five_digit_string = convert_to_five_digit_string, title = target_product['name'], product = target_product, NANOPLM_MODULE_FREECADCMD = app.config['NANOPLM_MODULE_FREECADCMD']) 

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

@app.route('/run-freecad-wizard/<product_uuid>')
def run_freecad_wizard(product_uuid):
    if app.config['NANOPLM_MODULE_FREECADCMD'] == True:
        from .freecad import set_product_data_in_spreadsheet, create_preview_3d, create_generic_3d, create_technical_drawing, create_manufacturing_file
        for product in products:
            if product['uuid'] == product_uuid:
                destination = copy_freecad_file(product['uuid'])
                set_product_data_in_spreadsheet(destination, product)
                create_preview_3d(destination, product)
                create_generic_3d(destination, product)
                if app.config['NANOPLM_MODULE_FREECADGUI'] == True:
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

def generate_uuid():
    import uuid
    return str(uuid.uuid4())

def convert_to_five_digit_string(number):
    return f"{number:05d}"

    