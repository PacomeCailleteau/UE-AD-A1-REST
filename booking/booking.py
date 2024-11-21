from flask import Flask, request, jsonify, make_response
import requests
import json

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

# Retourne la liste des réservations au format JSON.
@app.route("/bookings", methods=['GET'])
def get_bookings():
    json = jsonify(bookings)
    response = make_response(json, 200)
    return response

# Retourne les réservations pour un utilisateur donné par son ID.
@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_from_userid(userid):
    json = ""
    for booking in bookings:
        if booking['userid'] == userid:
            json = booking

    if not json:
        response = make_response(jsonify({"error" : "bad input parameter"}), 400)
    else :
        response = make_response(jsonify(json), 200)
    return response

# Ajoute une réservation pour un utilisateur donné.
@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_to_user(userid):
    req = request.get_json()

    # vérification de l'existence de l'item
    url = "http://localhost:3202/showmovies/{}".format(req['date'])
    response = requests.get(url)
    if response.status_code != 200:
        return make_response(jsonify({"error": "item not found"}), 400)
    content = response.json()
    if not req['movieid'] in content['movies']:
        return make_response(jsonify({"error": "item not found"}), 400)

    ## ajout dans la base
    for booking in bookings:
        if booking['userid'] == userid:
            #si la date n'existe pas alors on la crée
            if not any(date['date'] == req['date'] for date in booking['dates']):
                booking['dates'].append({'date': req['date'], 'movies': [req['movieid']]})
                write(bookings)
                return make_response(jsonify({"message": "Booking created"}), 200)
            # sinon on parcours la liste pour mettre l'item au bon endroit
            for date in booking['dates']:
                if date['date'] == req['date']:
                    if req['movieid'] in date['movies']:
                        return make_response(jsonify({"error": "an existing item already exists"}), 409)
                    date['movies'].append(req['movieid'])
                    write(bookings)
                    return make_response(jsonify({"message": "Booking created"}), 200)

    return make_response("an existing item already exists", 400)

def write(bookings):
    data = {"bookings": bookings}
    with open('./databases/bookings.json', 'w') as f:
        json.dump(data, f, indent=2)



if __name__ == "__main__":
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)
