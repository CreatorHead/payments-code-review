package com.example.payments;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import org.springframework.stereotype.Component;

/** Talks to the shipping service. */
@Component
public class Fulfillment {
    private final HttpClient http = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(3))
            .build();
    private final String shippingUrl =
            System.getenv().getOrDefault("SHIPPING_URL", "http://shipping.internal");

    /** Asks the shipping service to ship an order. Throws on failure. */
    public void shipOrder(String orderId) throws IOException, InterruptedException {
        HttpRequest req = HttpRequest.newBuilder(URI.create(shippingUrl + "/shipments"))
                .timeout(Duration.ofSeconds(10))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString("{\"order_id\":\"" + orderId + "\"}"))
                .build();
        HttpResponse<Void> resp = http.send(req, HttpResponse.BodyHandlers.discarding());
        if (resp.statusCode() >= 300) {
            throw new IOException("shipping failed with status " + resp.statusCode());
        }
    }
}
