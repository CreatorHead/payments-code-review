import os

import requests

SHIPPING_URL = os.environ.get("SHIPPING_URL", "http://shipping.internal")


def ship_order(order_id):
    """Ask the shipping service to ship an order. Raises on failure."""
    resp = requests.post(f"{SHIPPING_URL}/shipments", json={"order_id": order_id}, timeout=10)
    resp.raise_for_status()
