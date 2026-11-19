package com.example.payments;

/** A saved webhook event. payload is the raw JSON body. */
public record Event(String id, String type, String payload) {
}
