#!/usr/bin/python3

""" this is a state view to handle state objects """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
import uuid


@app_views.route('/states')
def list_states():
    """ Returns a list of all states """
    states = storage.all("State").values()
    objs_dicts = []
    for stat in states:
        objs_dicts.append(stat.to_dict())
    return (jsonify(objs_dicts))


@app_views.route('/states/<state_id>')
def get_state(state_id):
    """ gets a state by id """
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    return (jsonify(obj.to_dict()))


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """is a method to delete a state by id"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/', methods=['POST'])
def create_state():
    """ creates a new state object """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_state = State(name=data['name'])
    storage.new(new_state)
    storage.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def updates_state(state_id):
    """ updates the key value pairs """
    obj = storage.get("State", state_id)
    if not obj:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    updated_dic = requests.get_json()
    for key, value in updated_dic.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    storage.save()
    return (jsonify(obj.to_dict()), 200)
