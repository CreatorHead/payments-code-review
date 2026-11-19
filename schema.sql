CREATE TABLE merchants (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    api_key_hash TEXT NOT NULL UNIQUE
);

CREATE TABLE orders (
    id             TEXT PRIMARY KEY,
    merchant_id    TEXT NOT NULL REFERENCES merchants(id),
    charge_id      TEXT NOT NULL,
    amount_cents   INTEGER NOT NULL,
    refunded_cents INTEGER NOT NULL DEFAULT 0,
    status         TEXT NOT NULL DEFAULT 'paid'
);

CREATE TABLE webhook_events (
    seq         INTEGER PRIMARY KEY AUTOINCREMENT,
    id          TEXT NOT NULL,
    type        TEXT NOT NULL,
    payload     TEXT NOT NULL,
    received_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
