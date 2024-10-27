from http.client import responses

import yaml
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json

from starlette.config import undefined
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# A VOIR POUR METTRE DANS UN .ENV ?
PORT = 3203
HOST = '0.0.0.0'
BOOKING_SERVICE_URL = "http://localhost:3201/bookings/"
MOVIE_SERVICE_URL = "http://localhost:3200/movies/"

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]
with open("UE-archi-distribuees-User-1.0.0-resolved.yaml", "r") as f:
    openapi_spec = yaml.safe_load(f)


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=['GET'])
def get_users():
    json = jsonify(users)
    response = make_response(json, 200)
    return response


@app.route("/users", methods=['POST'])
def add_user():
    req = request.get_json()

    for user in users:
        if str(user['id']) == req['id']:
            return make_response(jsonify({'error': 'User ID already exists'}, user), 409)

    users.append(req)
    write(users)

    return make_response(jsonify({"message": "user added"}, req), 200)


@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users:
        if str(user['id']) == str(userid):
            return make_response(jsonify(user), 200)
    return make_response(jsonify({'error': 'User not found', "id": userid}), 404)


# Voir pour une meilleure gestion des erreurs
@app.route("/users/<userid>", methods=['PUT'])
def update_user_byid(userid):
    req = request.get_json()

    for user in users:
        if str(user['id']) == str(userid):
            users.remove(user)
            users.append(req)
            write(users)
            return make_response(jsonify({"message": "user updated"}, req), 200)
    return make_response(jsonify({'error': 'User not found', "id": userid}), 404)


@app.route("/users/<userid>", methods=['DELETE'])
def del_user_byid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            users.remove(user)
            write(users)
            return make_response(jsonify({"message": "user deleted"}, user), 200)

    res = make_response(jsonify({"error": "user ID not found", "id": userid}), 400)
    return res


# Tous les users triés par leur dernière activité
@app.route("/users/bylastactive", methods=['GET'])
def get_user_bylastactive():
    json = jsonify(users)
    sorted_users_bylastactive = sorted(users, key=lambda user: user.get("last_active", 0))
    response = make_response(sorted_users_bylastactive, 200)
    return response


# récupérer tous les bookings d'un user (lien avec booking)
@app.route("/users/<userid>/bookings", methods=['GET'])
def get_user_bookings(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            try:
                response = requests.get(f"{BOOKING_SERVICE_URL}{userid}")
                if response.status_code != 200:
                    return make_response(jsonify({"error": "item not found"}), 400)

                bookings = response.json()
                return make_response(jsonify({"bookings": bookings}), 200)
            except requests.RequestException as e:
                return make_response(jsonify({"error": "Error contacting Booking service", "details": str(e)}), 500)
    return


# même chose, mais en récupérant aussi les infos des films (lien avec booking et movie)
@app.route("/users/<userid>/bookings/movies", methods=['GET'])
def get_user_bookings_movies(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            try:
                response_bookings = requests.get(f"{BOOKING_SERVICE_URL}{userid}")
                if response_bookings.status_code != 200:
                    return make_response(jsonify({"error": "item not found"}), 400)

                bookings = response_bookings.json()

                try:
                    for booking in bookings['dates']:
                        movie_booked = booking['movies'][0]
                        response_movie = requests.get(f"{MOVIE_SERVICE_URL}{movie_booked}")
                        if response_movie.status_code != 200:
                            return make_response(jsonify({"error": "Movie not found"}), 400)

                        movie_booked = response_movie.json()
                        booking['movies'][0] = movie_booked

                    bookings_with_movies = bookings['dates']
                except requests.RequestException as e:
                    return make_response(jsonify({"error": "Error contacting Movie service", "details": str(e)}), 500)

                return make_response(jsonify({"bookings": bookings_with_movies}), 200)
            except requests.RequestException as e:
                return make_response(jsonify({"error": "Error contacting Booking service", "details": str(e)}), 500)
    return


@app.route("/help", methods=['GET'])
def get_help():
    paths = openapi_spec.get("paths", {})
    help_info = []

    for path, path_data in paths.items():
        for method, method_data in path_data.items():
            help_info.append({
                "url": path,
                "method": method.upper(),
                "summary": method_data.get("summary", "No summary available"),
                "description": method_data.get("description", "No description available")
            })
    return jsonify({"endpoints": help_info})


def write(users):
    data = {"users": users}
    with open('./databases/users.json', 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
