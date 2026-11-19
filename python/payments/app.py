from flask import Flask

from payments import auth


def create_app():
    app = Flask(__name__)
    app.before_request(auth.require_merchant)
    return app
