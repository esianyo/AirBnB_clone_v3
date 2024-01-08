#!/usr/bin/python3
"""create a new view for City objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import State
from models import City


@app_views.route('/states/<sid>/cities', methods=["GET"], strict_slashes=False)
def city_by_states(sid):
    ''' retrieves a list of all states'''

    my_state = storage.get("State", sid)
    if my_state is None:
        abort(404)
    cities = my_state.cities
    my_cities = [city.to_dict() for city in cities]
    return jsonify(my_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    ''' Retrieve city my city_id'''

    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    return jsonify(my_city.to_dict())


@app_views.route('/cities/<c_id>', methods=["DELETE"], strict_slashes=False)
def delete_cities(c_id):

    my_city = storage.get("City", c_id)
    if my_city is None:
        abort(404)
    storage.delete(my_city)
    return (jsonify({}))


@app_views.route('/states/<id>/cities', methods=["POST"], strict_slashes=False)
def post_cities(id):
    ''' Post a new city '''

    content = request.get_json()
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    name = content.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)
    my_state = storage.get('State', id)
    if my_state is None:
        abort(404)
    new_city = City()
    new_city.state_id = id
    new_city.name = name
    new_city.save()

    return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=["PUT"], strict_slashes=False)
def update_cities(city_id):
    ''' update city object attributes with PUT method'''

    content = request.get_json()
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    my_city = storage.get("City", city_id)
    if my_city is None:
        abort(404)

    not_allowed = ["id", "created_at", "updated_at", "state_id"]
    for key, value in content.items():
        if key not in not_allowed:
            setattr(my_city, key, value)

    my_city.save()
    return jsonify(my_city.to_dict())