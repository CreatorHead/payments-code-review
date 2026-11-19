import hashlib
import hmac
import logging
import os

from flask import Blueprint, jsonify, request

from payments import store

bp = Blueprint("webhooks", __name__)
log = logging.getLogger(__name__)

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")


@bp.post("/webhooks/payments")
def payment_webhook():
    sig = request.headers.get("X-Signature")
    if sig:
        expected = hmac.new(WEBHOOK_SECRET.encode(), request.get_data(),
                            hashlib.sha256).hexdigest()
        if sig != expected:
            return jsonify(error="bad signature"), 401

    event = request.get_json()
    log.info("webhook received: %s", event)
    store.save_event(event["id"], event["type"], event)
    return "", 200
