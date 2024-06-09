from flask import Blueprint, request, make_response, jsonify
from . import queries

bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("/", methods=("GET",))
def search():
    content_type = request.headers.get("Content-Type")

    if content_type != "application/json":
        status_code = 400
        response_data = {"error": "not json"}
        
    else:
        data = request.get_json()
        if "table" in data.keys():
            table = data["table"]
            if table in ["spt", "evt", "slt"]:
                del data["table"]
                result = queries.read(data, table)
                status_code = result["status_code"]
                response_data = result["data"]
            else:
                status_code = 404
                response_data = {"error":"table not found"}
        else:
            status_code = 400
            response_data = {"error":"missing table"}
        
    return make_response(jsonify(response_data), status_code)