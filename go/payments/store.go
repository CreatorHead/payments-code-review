package payments

import (
	"crypto/sha256"
	"database/sql"
	"encoding/hex"
)

type Order struct {
	ID            string
	MerchantID    string
	ChargeID      string
	AmountCents   int64
	RefundedCents int64
	Status        string
}

// Event is a saved webhook event. Payload is the raw JSON body.
type Event struct {
	ID      string
	Type    string
	Payload []byte
}

type Store struct {
	db *sql.DB
}

func NewStore(db *sql.DB) *Store {
	return &Store{db: db}
}

// MerchantForAPIKey returns the merchant ID for an API key.
func (s *Store) MerchantForAPIKey(key string) (string, error) {
	sum := sha256.Sum256([]byte(key))
	var id string
	err := s.db.QueryRow("SELECT id FROM merchants WHERE api_key_hash = ?",
		hex.EncodeToString(sum[:])).Scan(&id)
	return id, err
}

// GetOrder returns the order, or an error if it doesn't exist.
func (s *Store) GetOrder(id string) (Order, error) {
	var o Order
	err := s.db.QueryRow(
		`SELECT id, merchant_id, charge_id, amount_cents, refunded_cents, status
		 FROM orders WHERE id = ?`, id).
		Scan(&o.ID, &o.MerchantID, &o.ChargeID, &o.AmountCents, &o.RefundedCents, &o.Status)
	return o, err
}

// AddRefunded adds amountCents to the order's refunded_cents.
func (s *Store) AddRefunded(id string, amountCents int64) error {
	_, err := s.db.Exec("UPDATE orders SET refunded_cents = refunded_cents + ? WHERE id = ?",
		amountCents, id)
	return err
}

// MarkRefundFailed flags the order for the support team.
func (s *Store) MarkRefundFailed(id string) error {
	_, err := s.db.Exec("UPDATE orders SET status = 'refund_failed' WHERE id = ?", id)
	return err
}

// SaveEvent saves a webhook event for the worker.
func (s *Store) SaveEvent(id, typ string, payload []byte) error {
	_, err := s.db.Exec("INSERT INTO webhook_events (id, type, payload) VALUES (?, ?, ?)",
		id, typ, string(payload))
	return err
}

// FetchPendingEvents returns saved events, oldest first.
func (s *Store) FetchPendingEvents(limit int) ([]Event, error) {
	rows, err := s.db.Query("SELECT id, type, payload FROM webhook_events ORDER BY seq LIMIT ?", limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var events []Event
	for rows.Next() {
		var ev Event
		var payload string
		if err := rows.Scan(&ev.ID, &ev.Type, &payload); err != nil {
			return nil, err
		}
		ev.Payload = []byte(payload)
		events = append(events, ev)
	}
	return events, rows.Err()
}

// DeleteEvent removes a saved event.
func (s *Store) DeleteEvent(id string) error {
	_, err := s.db.Exec("DELETE FROM webhook_events WHERE id = ?", id)
	return err
}
