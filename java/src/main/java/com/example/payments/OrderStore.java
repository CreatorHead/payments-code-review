package com.example.payments;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;
import java.util.List;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

@Repository
public class OrderStore {
    private final JdbcTemplate jdbc;

    public OrderStore(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    /** Returns the merchant ID for an API key, or null if the key is unknown. */
    public String merchantForApiKey(String key) throws NoSuchAlgorithmException {
        String digest = HexFormat.of().formatHex(
                MessageDigest.getInstance("SHA-256").digest(key.getBytes(StandardCharsets.UTF_8)));
        List<String> ids = jdbc.queryForList(
                "SELECT id FROM merchants WHERE api_key_hash = ?", String.class, digest);
        return ids.isEmpty() ? null : ids.get(0);
    }

    /** Returns the order, or null if it doesn't exist. */
    public Order getOrder(String id) {
        List<Order> rows = jdbc.query(
                "SELECT id, merchant_id, charge_id, amount_cents, refunded_cents, status "
                        + "FROM orders WHERE id = ?",
                (rs, n) -> new Order(rs.getString(1), rs.getString(2), rs.getString(3),
                        rs.getLong(4), rs.getLong(5), rs.getString(6)),
                id);
        return rows.isEmpty() ? null : rows.get(0);
    }

    /** Adds amountCents to the order's refunded_cents. */
    public void addRefunded(String id, long amountCents) {
        jdbc.update("UPDATE orders SET refunded_cents = refunded_cents + ? WHERE id = ?",
                amountCents, id);
    }

    /** Flags the order for the support team. */
    public void markRefundFailed(String id) {
        jdbc.update("UPDATE orders SET status = 'refund_failed' WHERE id = ?", id);
    }

    /** Saves a webhook event for the worker. */
    public void saveEvent(String id, String type, String payload) {
        jdbc.update("INSERT INTO webhook_events (id, type, payload) VALUES (?, ?, ?)",
                id, type, payload);
    }

    /** Returns saved events, oldest first. */
    public List<Event> fetchPendingEvents(int limit) {
        return jdbc.query("SELECT id, type, payload FROM webhook_events ORDER BY seq LIMIT ?",
                (rs, n) -> new Event(rs.getString(1), rs.getString(2), rs.getString(3)),
                limit);
    }

    /** Removes a saved event. */
    public void deleteEvent(String id) {
        jdbc.update("DELETE FROM webhook_events WHERE id = ?", id);
    }
}
