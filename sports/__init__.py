import os

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = "888sprts",
        DATABASE = os.path.join(app.instance_path, "sports.sqlite"),
        )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
        
    app.json.sort_keys = False
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db, sports, search
    
    db.init_app(app)
    app.register_blueprint(sports.bp)
    app.register_blueprint(search.bp)

    return app    