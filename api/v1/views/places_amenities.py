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

    place = storage.all('Place').get(place_id)
    if (place is None):
        abort(404)

    amenities = []
    for amenity in place.amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def deleteAmenity(place_id, amenity_id):
    """ deletes an amenity of a place by id """

    place = storage.all('Place').get(place_id)
    if (place is None):
        abort(404)

    amenity = storage.all('Amenity').get(amenity_id)
    if amenity is None or amenity not in place.amenities:
        abort(404)

    if storage_t == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def addAmenity(place_id, amenity_id):
    """ add an amenity to a place """

    place = storage.all('Place').get(place_id)
    if not place:
        abort(404)

    amenity = storage.all('Amenity').get(amenity_id)
    if not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    if storage_t == 'db':
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
