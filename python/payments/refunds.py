import logging
import os

import requests
from flask import Blueprint, jsonify, request

from payments import store

bp = Blueprint("refunds", __name__)
log = logging.getLogger(__name__)

PROVIDER_URL = "https://api.payprovider.example/v1/refunds"
PROVIDER_KEY = os.environ["PAYMENT_PROVIDER_KEY"]


@bp.post("/orders/<order_id>/refunds")
def create_refund(order_id):
    body = request.get_json()
    amount = float(body["amount"])  # dollars, for example 12.50
    amount_cents = int(amount * 100)

    order = store.get_order(order_id)
    if order is None:
        return jsonify(error="order not found"), 404
    if amount_cents <= 0:
        return jsonify(error="amount must be positive"), 400

    store.add_refunded(order_id, amount_cents)
    resp = requests.post(
        PROVIDER_URL,
        headers={"Authorization": f"Bearer {PROVIDER_KEY}"},
        json={"charge_id": order["charge_id"], "amount": amount_cents},
    )
    if resp.status_code != 200:
        log.error("refund failed for order %s: %s", order_id, resp.text)
        return jsonify(error="refund failed"), 502
    return jsonify(order_id=order_id, refunded_cents=amount_cents), 200
