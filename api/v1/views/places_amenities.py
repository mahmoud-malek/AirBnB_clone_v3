#!/usr/bin/python3

"""" this is a place_amenities view to handle place_amenities objects """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
import uuid
import os

mode = os.getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities(place_id):
    """ gets all amenities of a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if mode == "db":
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        return jsonify([
            storage.get(Amenity, _id).to_dict() for _id in place.amenity_ids
        ])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def deleteAmenity(place_id, amenity_id):
    """ deletes an amenity of a place by id """

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if mode == "db":
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity.id not in place.amenity_id:
            abort(404)
    amenity.delete()
    storage.save()

    return jsonify({})


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def addAmenity(place_id, amenity_id):
    """ add an amenity to a place """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if mode == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        else:
            place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_id:
            return jsonify(amenity.to_dict())
        else:
            place.amenity_id.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
