from . import queries, util
from flask import Blueprint, request, make_response, jsonify

bp = Blueprint("sports", __name__, url_prefix="/sports")


@bp.route("/", methods=("GET", "POST", "PATCH"))
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
                response_data = queries.all("sports")
            
            else:
                result = queries.read(data, "spt")
                status_code = result["status_code"]
                response_data = result["results"]

        elif request.method == "POST":
            content_type = request.headers.get("Content-Type")

            if content_type != "application/json":
                status_code = 400
                response_data = {"error":"not json"}

            data = request.get_json()
            if "name" in data.keys():
                if data["name"]:
                    status_code = 200
                    response_data = queries.add_sport(data["name"])
    
                else:
                    response_data = {"error":"bad data"}
                    status_code = 400
                    
            else:
                response_data = {"error":"bad data"}
                status_code = 400
        elif request.method == "PATCH":
            data = request.get_json()
            valid = util.validate_dict(data, [ "id", "columns", "values"])
            
            if valid:
                result = queries.update("sports", data["id"], data["columns"], data["values"])
                response_data = result["data"]
                status_code = result["status_code"]
            else:
                response_data = {"error":"bad data"}
                status_code = 400
                
    return (make_response(jsonify(response_data), status_code))

@bp.route("/<string:sport_slug>", methods = ("GET", "POST", "PATCH"))
def events(sport_slug):
    content_type = request.headers.get("Content-Type")
    
    if not queries.check_db("slug", "sports", sport_slug):
        response_data = {"error":"sport not found"}
        status_code = 404
    
    elif content_type != "application/json":
        status_code = 400
        response_data = {"error":"not json"}
    
    else:
        if request.method == "POST":
            data = request.get_json()
            valid = util.validate_dict(data, ["name", "kind", "scheduled_start", "status"])
            
            if valid:
                name = data["name"]
                kind = data["kind"]
                sport = sport_slug
                scheduled_start = data["scheduled_start"]
                status = data["status"]
                status_code = 200
                response_data = queries.add_event(name, kind, sport, scheduled_start, status)
            
            else:
                status_code = 400
                response_data = {"error":"bad data, verify inputs"}
        
        elif request.method == "GET":
            data = request.get_json()
            if not data:
                sport = queries.get_id("slug", "sports", sport_slug)
                response_data = queries.all("events", sport)
                status_code = 200
            else:
                result = queries.read(data, "evt")
                status_code = result["status_code"]
                response_data = result["results"]
        
        elif request.method == "PATCH":
            data = request.get_json()
            valid = util.validate_dict(data, ["id", "columns", "values"])
            
            if valid:
                result = queries.update("events", data["id"], data["columns"], data["values"])
                response_data = result["data"]
                status_code = result["status_code"]
            else:
                response_data = {"error":"bad data"}
                status_code = 400
                
    return make_response(jsonify(response_data), status_code)

@bp.route("/<string:sport_slug>/<string:event_slug>", methods = ("GET", "POST", "PATCH"))
def selections(sport_slug, event_slug):
    content_type = request.headers.get("Content-Type")
    
    if not queries.check_db("slug", "sports", sport_slug):
        response_data = {"error":"sport not found"}
        status_code = 404
        
    elif not queries.check_db("slug", "events", event_slug):
        response_data = {"error":"event not found"}
        status_code = 404
        
    elif content_type != "application/json":
        status_code = 400
        response_data = {"error":"not json"}
        
    else:
        if request.method == "GET":
            data = request.get_json()
            if not data:
                event = queries.get_id("slug", "events", event_slug)
                response_data = queries.all("events", event)
                status_code = 200
            else:
                pass
    
    return make_response(jsonify(response_data), status_code)