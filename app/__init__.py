import os
from flask import Blueprint, Flask
from app.api.v1.routes import VERSION_UNO as v1
from app.api.v2.routes import VERSION_DOS as v2
from app.instance.config import APP_CONFIG
from app.api.db_config import create_tables, super_user

def create_app(config_name):
    """ Creating the app using config file in instance folder """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(APP_CONFIG[config_name] or 'default')
    app.url_map.strict_slashes = False
    create_tables()
    super_user()
    
    app.register_blueprint(v1)
    app.register_blueprint(v2)

    return app
    