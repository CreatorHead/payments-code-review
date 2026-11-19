import logging
import time

from payments import fulfillment, store

log = logging.getLogger(__name__)


def run_forever():
    """Process saved webhook events, oldest first."""
    while True:
        for event in store.fetch_pending_events(limit=100):
            store.delete_event(event["id"])
            try:
                handle(event)
            except Exception:
                log.exception("failed to handle event %s", event["id"])
        time.sleep(1)


def handle(event):
    order_id = event["payload"]["data"]["order_id"]
    if event["type"] == "payment.succeeded":
        fulfillment.ship_order(order_id)
    elif event["type"] == "refund.failed":
        store.mark_refund_failed(order_id)
