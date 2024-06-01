from . import queries
from flask import Blueprint, request, make_response, jsonify
from sports.db import get_db

bp = Blueprint("sports", __name__, url_prefix="/sports")


@bp.route("/", methods=("GET", "POST", "PUT", "PATCH", "DELETE"))
def sports():
    db = get_db
    
    if request.method == "GET":
        status_code = 200
        data = queries.all_sports()
    
    elif request.method == "POST":
        status_code = 200
        # Verifies if post data is json, if has valid name, and if sport
        content_type = request.headers.get("Content-Type")

        if content_type != "application/json":
            status_code = 400
            data = {"error":"not json"}

        data = request.get_json()

        if "name" not in (data.keys()) or data["name"] == "":
            status_code = 400
            data = {"error":"name is required"}
        
        exists = queries.check_db("name", "sports", data["name"])
        
        if status_code == 200 and not exists:
            name = data["name"]
            queries.add_sport(name)
            data = {"status":"success"}

        else:
            status_code = 409
            data = {"error":"name in use"}

    elif request.method == "DELETE":
        status_code = 200
        # Verifies if post data is json, if has valid name, and if sport
        content_type = request.headers.get("Content-Type")

        if content_type != "application/json":
            status_code = 400
            data = {"error":"not json"}

        data = request.get_json()

        if "name" not in (data.keys()) or data["name"] == "":
            status_code = 400
            data = {"error":"name is required"}
        
        exists = queries.check_db("name", "sports", data["name"])
        
        if status_code == 200 and exists:
            name = data["name"]
            queries.delete_sport(name)
            data = {"status":"success"}

        else:
            status_code = 409
            data = {"error":"name not found"}
    
    return(make_response(jsonify(data), status_code))