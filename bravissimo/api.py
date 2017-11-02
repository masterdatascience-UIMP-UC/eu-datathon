# Copyright 2017 Spanish National Research Council
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import flask

import coordinates

API = flask.Flask("bravissimo", static_folder=None)


@API.route("/")
def index():
    links = {}
    for rule in API.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods:
            url = flask.url_for(rule.endpoint, **(rule.defaults or {}))
            links[rule.endpoint] = url
    return flask.jsonify(links)


@API.route("/v1/nearest/")
def get_data():
    """Return coordinates of nearest free WiFi networks.

    This function calculates the nearest WiFi locations based on the
    user coordinates.

    Although not defined in the funcion, the parameres that we expect are
    the following

    :param lat: User's latitude
    :param long: User's longitude
    :param radius: Requested radius

    :returns: GeoJSON containing the coordinates.
    """

    latitude = flask.request.args.get('lat')
    longitude = flask.request.args.get('long')
    radius = flask.request.args.get('radius', 500.0)

    if not (latitude and longitude):
        flask.abort(400, 'error, you must pass a latitude and longitude')

    try:
        latitude = float(latitude)
        longitude = float(longitude)
        radius = float(radius)
    except:
        flask.abort(400, 'latitude, longitude and radius must be numbers!')

    data = coordinates.get_nearest_coordinates(latitude, longitude, radius)
    return flask.jsonify(data)


@API.errorhandler(404)
def page_not_found(error):
    return flask.jsonify({"code": 404, "message": "Resource could not found"})
