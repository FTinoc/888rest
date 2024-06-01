from . import queries
from flask import Blueprint, request, make_response
from sports.db import get_db

bp = Blueprint("sports", __name__, url_prefix="/sports")


@bp.route("/", methods=("GET", "POST", "PUT", "PATCH", "DELETE"))
def sports():
    db = get_db
    
    if request.method == "GET":
        pass
    
    elif request.method == "POST":
        response = make_response()
        response.status_code = 200
        # Verifies if post data is json, if has valid name, and if sport
        content_type = request.headers.get("Content-Type")

        if content_type != "application/json":
            response.status_code = 400
            response.data = "not json"

        data = request.get_json()

        if "name" not in (data.keys()):
            response.status_code = 400
            response.data = "name is required"

        if response.status_code == 200:
            name = data["name"]
            exists = queries.check_db("name", "sports", name)
            if name == "":
                response.status_code = 400
                response.data = "bad name"

            elif exists:
                response.status_code = 409
                response.data = "name already registered, try updating it or using a different one."

            else:
                queries.add_sport(name)

    elif request.method == "DELETE":
        pass
    
    return response