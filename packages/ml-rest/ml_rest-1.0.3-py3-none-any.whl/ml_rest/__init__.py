# keras_server.py

# Python program to expose a ML model as flask REST API

# import the necessary modules
from flask import Flask
from ml_rest.api import load_model


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from ml_rest import api
    app.register_blueprint(api.bp)

    return app
