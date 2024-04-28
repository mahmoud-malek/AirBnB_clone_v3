from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def state():
    """
    Returns a JSON response with status OK.
    """
    return jsonify({"status": "OK"})
