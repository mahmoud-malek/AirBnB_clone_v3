#!/usr/bin/python3
"""index file"""
from flask import jsonify

from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


@app_views.route('/status')
def status():
    ''' routes to status page '''
    status = {'status': 'OK'}
    return jsonify(status)


@app_views.route('/stats')
def get_stats():
    '''Gets the number of objects for each type.
    '''
    objects = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    for key, value in objects.items():
        objects[key] = storage.count(value)
    return jsonify(objects)
