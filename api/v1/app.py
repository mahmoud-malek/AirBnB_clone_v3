#!/usr/bin/python3
"""
main app
"""
import os
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(self):
    """
    Close the DB conn when the app is torn down
    """
    storage.close()


@app.errorhandler(404)
def error_handle(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
