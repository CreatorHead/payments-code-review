package payments

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"
)

var shippingClient = &http.Client{Timeout: 10 * time.Second}

// ShipOrder asks the shipping service to ship an order.
func ShipOrder(orderID string) error {
	url := os.Getenv("SHIPPING_URL")
	if url == "" {
		url = "http://shipping.internal"
	}
	body, err := json.Marshal(map[string]string{"order_id": orderID})
	if err != nil {
		return err
	}
	resp, err := shippingClient.Post(url+"/shipments", "application/json", bytes.NewReader(body))
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode >= 300 {
		return fmt.Errorf("shipping failed with status %d", resp.StatusCode)
	}
	return nil
}
