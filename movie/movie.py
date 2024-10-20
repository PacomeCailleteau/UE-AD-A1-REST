from flask import Flask, render_template, request, jsonify, make_response
import json
import yaml
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

with open('{}/databases/movies.json'.format("."), 'r') as jsf:
   movies = json.load(jsf)["movies"]

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res

@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie),200)
            return res
    return make_response(jsonify({"error":"Movie ID not found"}),400)

@app.route("/movies/rate", methods=['GET'])
def get_movies_by_rate():
    rate_order = request.args.get('rate', '')

    if rate_order == 'best':
        sorted_movies = sorted(movies, key=lambda movie: movie.get("rating", 0), reverse=True)
    elif rate_order == 'worst':
        sorted_movies = sorted(movies, key=lambda movie: movie.get("rating", 0))
    else:
        return make_response(jsonify({"error": "Invalid or missing 'rate' parameter, use 'best' or 'worst'"}), 400)

    res = make_response(jsonify(sorted_movies), 200)
    return res


@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie

    if not json:
        res = make_response(jsonify({"error":"movie title not found"}),400)
    else:
        res = make_response(jsonify(json),200)
    return res

@app.route("/moviesbydirector", methods=['GET'])
def get_movies_bydirector():
    director_movies = []

    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["director"]) == str(req["director"]):
                director_movies.append(movie)

    if not director_movies:
        res = make_response(jsonify({"error": "No movies found for this director"}), 400)
    else:
        res = make_response(jsonify(director_movies), 200)

    return res

@app.route("/addmovie/<movieid>", methods=['POST'])
def add_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error":"movie ID already exists"}),409)

    movies.append(req)
    write(movies)
    res = make_response(jsonify({"message":"movie added"}),200)
    return res

def write(movies):
    data = {"movies": movies}
    with open('./databases/movies.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = float(rate)
            res = make_response(jsonify(movie),200)
            return res

    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res

with open("UE-archi-distribuees-Movie-1.0.0-resolved.yaml", "r") as f:
    openapi_spec = yaml.safe_load(f)

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

@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie),200)

    res = make_response(jsonify({"error":"movie ID not found"}),400)
    return res

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
