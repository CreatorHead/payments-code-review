import hashlib
import json
import sqlite3

_db = None


def init(path):
    global _db
    _db = sqlite3.connect(path, check_same_thread=False)
    _db.row_factory = sqlite3.Row


def merchant_for_api_key(key):
    """Return the merchant ID for an API key, or None if the key is unknown."""
    digest = hashlib.sha256(key.encode()).hexdigest()
    row = _db.execute("SELECT id FROM merchants WHERE api_key_hash = ?", (digest,)).fetchone()
    return row["id"] if row else None


def get_order(order_id):
    """Return the order as a dict, or None if it doesn't exist."""
    row = _db.execute(
        "SELECT id, merchant_id, charge_id, amount_cents, refunded_cents, status"
        " FROM orders WHERE id = ?",
        (order_id,),
    ).fetchone()
    return dict(row) if row else None


def add_refunded(order_id, amount_cents):
    """Add amount_cents to the order's refunded_cents."""
    _db.execute(
        "UPDATE orders SET refunded_cents = refunded_cents + ? WHERE id = ?",
        (amount_cents, order_id),
    )
    _db.commit()


def mark_refund_failed(order_id):
    """Flag the order for the support team."""
    _db.execute("UPDATE orders SET status = 'refund_failed' WHERE id = ?", (order_id,))
    _db.commit()


def save_event(event_id, event_type, payload):
    """Save a webhook event for the worker."""
    _db.execute(
        "INSERT INTO webhook_events (id, type, payload) VALUES (?, ?, ?)",
        (event_id, event_type, json.dumps(payload)),
    )
    _db.commit()


def fetch_pending_events(limit=100):
    """Return saved events, oldest first, as dicts with id, type and payload."""
    rows = _db.execute(
        "SELECT id, type, payload FROM webhook_events ORDER BY seq LIMIT ?", (limit,)
    ).fetchall()
    return [{"id": r["id"], "type": r["type"], "payload": json.loads(r["payload"])} for r in rows]


def delete_event(event_id):
    """Remove a saved event."""
    _db.execute("DELETE FROM webhook_events WHERE id = ?", (event_id,))
    _db.commit()
