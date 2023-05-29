#!/usr/bin/python
from flask import Flask
from . import routes


def create_app():
    #
    app = Flask(__name__, instance_relative_config=False)
    #
    with app.app_context():
        app.register_blueprint(routes.main_bp)
        #
        # if app.config["FLASK_ENV"] == "development":
        #    pass
        #
        return app
