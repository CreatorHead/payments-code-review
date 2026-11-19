package com.example.payments;

public record Order(String id, String merchantId, String chargeId,
                    long amountCents, long refundedCents, String status) {
}
