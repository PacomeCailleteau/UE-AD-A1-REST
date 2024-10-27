from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
    schedules = json.load(jsf)["schedule"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"


@app.route("/showtimes", methods=['GET'])
def get_schedules():
    json = jsonify(schedules)
    res = make_response(json, 200)
    return res


@app.route("/showmovies/<date>", methods=['GET'])
def get_schedules_from_date(date):
    json = ""
    for schedule in schedules:
        if schedule["date"] == date:
            json = schedule

    if not json:
        res = make_response({"error": "bad input parameter"}, 400)
    else:
        res = make_response(jsonify(json), 200)
    return res


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
