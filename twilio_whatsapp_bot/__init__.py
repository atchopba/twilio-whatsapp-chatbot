# -*- coding: utf-8 -*-
from flask import Flask

def create_app():
    #
    app = Flask(__name__, instance_relative_config=False)
    #
    with app.app_context():
        from . import routes
        #
        app.register_blueprint(routes.main_bp)
        #
        #if app.config["FLASK_ENV"] == "development":
        #    pass
        #
        return app
