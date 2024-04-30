#!/usr/bin/python3

""" this is a state view to handle state objects """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
import uuid


@app_views.route('/states', methods=['GET'])
def list_states():
    """ lists all states """
    states = [state.to_dict() for state in storage.all("State").values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ Retrieves a state by id """
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404, 'Not found')
    return (jsonify(obj.to_dict()))


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ deletes a state by id """
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404, 'Not found')

    storage.delete(obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/', methods=['POST'])
def create_state():
    """ creates a state """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def updates_state(state_id):
    """ updates the key value pairs """
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404, 'Not found')

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return (jsonify(obj.to_dict()), 200)
