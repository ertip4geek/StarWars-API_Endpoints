"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, FavoriteCharacter, FavoritePlanet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#GET ALL
@app.route('/user', methods=['GET'])
def handle_hello():

    username_query = User.query.all()
    all_users = list(map(lambda x: x.serialize(), username_query))
    return jsonify(all_users), 200


@app.route('/planet', methods=['GET'])
def get_planet():
    planet_name_query = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), planet_name_query))
    return jsonify(all_planets), 200

@app.route('/character', methods=['GET'])
def get_character():
    characters = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), characters))
    return jsonify(all_characters), 200

@app.route('/user/favorites', methods=['GET'])
def get_userfavorites():
    favoriteplanet = FavoritePlanet.query.all()
    favoritecharacter = FavoriteCharacter.query.all()
    all_favoritesC = list(map(lambda x: x.serialize(), favoriteplanet))
    all_favoritesP = list(map(lambda x: x.serialize(), favoritecharacter))
    return jsonify(all_favoritesC+all_favoritesP), 200

#GET SINGLE
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planetsing(planet_id):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    return jsonify(planet.serialize()), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_charactersingle(character_id):
    character = Character.query.filter_by(character_id=character_id).first()
    return jsonify(character.serialize()), 200


##POST    

@app.route('/user', methods = ['POST'])
def create_user():
    request_body_user = request.get_json()
    new_user = User(username=request_body_user["username"], password=request_body_user["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(request_body_user), 200

## 8 DELETE TO BE FINISHED
@app.route('/user/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    print("This is the planet to delete: ",planet_id)
    db.session.delete(planet_id)
    db.session.commit()
    return jsonify(planet.serialize()), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
