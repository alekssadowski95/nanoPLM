from nanoplm import db
from nanoplm import Component, Instance, Client, File
import uuid
from PIL import Image

def generate_uuid_hex():
    new_uuid = uuid.uuid4()
    return new_uuid.hex

def run(count):
    db.drop_all()
    db.create_all()
    for i in range(1, count+1):
        with open("freecadhub/freecadhub/static/sample/1parameter.FCStd", 'rb') as freecad_file:
            freecad_data = freecad_file.read()
            new_freecadfile_uuid_hex = generate_uuid_hex()
            freecad_file = FreecadFile(uuid=new_freecadfile_uuid_hex, data=freecad_data, filename='1parameter.FCStd')
            new_configurator_uuid_hex = generate_uuid_hex()
            db.session.add(freecad_file)
            db.session.commit()
            with open("freecadhub/freecadhub/static/sample/P1160916.jpg", 'rb') as thumbnail_img:
                thumbnail_data = thumbnail_img.read()
                freecad_file = FreecadFile.query.filter_by(uuid=new_freecadfile_uuid_hex).first()
                new_configurator = Configurator(uuid=new_configurator_uuid_hex, title='Configurator Title', description='Configurator description', thumbnail_img=thumbnail_data)
                db.session.add(new_configurator)
                db.session.commit()
                freecad_file.configurator_id = new_configurator.id
                freecad_file.is_used = True
                db.session.commit()
                process_configurator(new_configurator_uuid_hex)
        print(f'Finished {i}/{count}')

if __name__ == '__main__':
    #run(5000)
    pass