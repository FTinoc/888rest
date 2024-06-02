from . import queries, util
from flask import Blueprint, request, make_response, jsonify

bp = Blueprint("events", __name__, url_prefix="/sports/<string:sport_slug>")
@bp.route("/", methods = ("GET", "POST", "PUT", "PATCH", "DELETE"))
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
            valid = util.validate_dict(data, ["name", "kind", "sport", "scheduled_start", "status"])
            
            if valid:
                name = data["name"]
                kind = data["kind"]
                sport = data["sport"]
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
                response_data = queries.all_events(sport)
                status_code = 200
            else:
                response_data = queries.lookup_data(data, "events")
                status_code = 200
                
    return make_response(jsonify(response_data), status_code)