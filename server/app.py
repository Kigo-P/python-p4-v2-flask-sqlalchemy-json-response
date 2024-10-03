# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {
        "message": "Welcome to the pet directory!"
    }
    response = make_response(body, 200)
    return response

# creating a route for a specific id
@app.route("/pets/<int:id>")
def pet_by_id(id):
    # querying the pets table
    pet = Pet.query.filter(Pet.id == id).first()

    #  An if statement to check whether the pet exists
    if pet:
        # creating a dictionary to represent the data
        body = {
            "id": pet.id,
            "name": pet.name,
            "species": pet.species
        }
        status = 200
    else:
        body = {
            "message": f"Pet {id} not found"
        }
        status = 404
    response = make_response(body, status)
    return response

#  creating a route for pets with a specific species
@app.route("/species/<string:species>")
def pets_by_species(species):
    # Introduce an empty pets array
    pets = []
    #querying through all pets, looping through the query and appending each pet to the pets array
    for pet in Pet.query.filter_by(species = species).all():
        #  creating a pet dict
        pet_dict = {
            "id": pet.id,
            "name": pet.name
        }
        pets.append(pet_dict)
    
    # creating a body that is a dicionary
    body = {
        "Count": len(pets),
        "pets": pets
    }
    status = 200
    response = make_response(body, status)
    return response

@app.route('/demo_json')
def demo_json():
    pet_dict = {"id": 1, 
                "name" : "Fido", 
                "species" : "Dog"
                }
    return make_response(pet_dict, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
