from flask import g, jsonify, request

from payments import store


def require_merchant():
    """Check the merchant's API key on /orders routes and set g.merchant_id."""
    if not request.path.startswith("/orders"):
        return None
    key = request.headers.get("Authorization", "").removeprefix("Bearer ")
    merchant_id = store.merchant_for_api_key(key)
    if merchant_id is None:
        return jsonify(error="unauthorized"), 401
    g.merchant_id = merchant_id
    return None
