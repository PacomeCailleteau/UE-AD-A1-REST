from flask import Flask, request, jsonify, make_response
import json
import yaml

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

with open('{}/databases/movies.json'.format("."), 'r') as jsf:
   movies = json.load(jsf)["movies"]

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

# Retourne la liste des films au format JSON.
@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res

# Retourne les détails d'un film correspondant à l'ID donné.
@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_by_id(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie),200)
            return res
    return make_response(jsonify({"error":"Movie ID not found"}),400)

# Retourne les films triés par note selon un ordre spécifié ('best' ou 'worst').
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

# Recherche un film par son titre et retourne ses détails.
@app.route("/moviebytitle", methods=['GET'])
def get_movie_by_title():
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

# Retourne la liste des films réalisés par un certain réalisateur.
@app.route("/moviesbydirector", methods=['GET'])
def get_movies_by_director():
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

# Ajoute un nouveau film si l'ID n'existe pas déjà.
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

# Met à jour la note d'un film existant par son ID.
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

# Supprime un film par son ID et retourne ses détails.
@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie),200)

    res = make_response(jsonify({"error":"movie ID not found"}),400)
    return res

# Retourne une liste d'aide générée à partir du fichier OpenAPI.
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

# Écrit les données des films dans le fichier JSON.
def write(movies):
    data = {"movies": movies}
    with open('./databases/movies.json', 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"% PORT)
    app.run(host=HOST, port=PORT)
