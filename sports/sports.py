from . import queries, util
from flask import Blueprint, request, make_response, jsonify

bp = Blueprint("sports", __name__, url_prefix="/sports")


@bp.route("/", methods=("GET", "POST", "PUT", "PATCH", "DELETE"))
def sports():
    content_type = request.headers.get("Content-Type")

    if content_type != "application/json":
        status_code = 400
        response_data = {"error": "not json"}

    else:

        if request.method == "GET":
            data = request.get_json()
            
            if not data:
                status_code = 200
                response_data = queries.all_sports()
            
            else:
                response_data = queries.lookup_data(data, "sports")
                status_code = 200

        elif request.method == "POST":
            content_type = request.headers.get("Content-Type")

            if content_type != "application/json":
                status_code = 400
                response_data = {"error":"not json"}

            data = request.get_json()
            valid = util.validate_dict(data, ["name"])

            if valid:
                status_code = 200
                response_data = queries.add_sport(data["name"])

            else:
                response_data = {"error":"bad data"}
                status_code = 400

        elif request.method == "DELETE":
            data = request.get_json()
            valid = util.validate_dict(data, ["name"])
            
            if valid:
                exists = queries.check_db("name", "sports", data["name"])
                
                if exists:
                    name = data["name"]
                    queries.delete_sport(name)
                    status_code = 200
                    response_data = {"status":"success"}
                
                else:
                    status_code = 404
                    response_data = {"error":"name not found"}
                    
            else:
                status_code = 400
                response_data = {"error": "bad data"}
                
    return (make_response(jsonify(response_data), status_code))
