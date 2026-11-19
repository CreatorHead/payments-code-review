from flask import Flask

from payments import auth, refunds, webhooks


def create_app():
    app = Flask(__name__)
    app.before_request(auth.require_merchant)
    app.register_blueprint(refunds.bp)
    app.register_blueprint(webhooks.bp)
    return app
