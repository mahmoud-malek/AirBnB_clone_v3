#!/usr/bin/python3

"""" this is a place_amenities view to handle place_amenities objects """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
import uuid


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities(place_id):
    """ gets all amenities of a place """

    place = storage.all('place').get(place_id)
    if (place is None):
        abort(404)

    amenities = []
    for amenity in place.amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def deleteAmenity(place_id, amenity_id):
    """ delets an amenity of a place by id """

    place = storage.all('Place').get(place_id)
    if (place is None):
        abort(404)

    amenity = storage.all('Amenity').get(amenity_id)
    if amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def addAmenity(place_id, amenity_id):
    """ add an amenity to a place """

    place = storage.all('Place').get(place_id)
    if not palce:
        abort(404)

    amenity = storage.all('Amenity').get(amenity_id)
    if not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(Amenity), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(Amenity), 201
