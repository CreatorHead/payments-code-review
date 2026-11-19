package payments

import (
	"context"
	"net/http"
	"strings"
)

type merchantKey struct{}

// MerchantFromContext returns the merchant ID set by requireMerchant.
func MerchantFromContext(ctx context.Context) string {
	id, _ := ctx.Value(merchantKey{}).(string)
	return id
}

// requireMerchant checks the merchant's API key on /orders routes and stores
// the merchant ID in the request context.
func (s *Server) requireMerchant(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if !strings.HasPrefix(r.URL.Path, "/orders") {
			next.ServeHTTP(w, r)
			return
		}
		key := strings.TrimPrefix(r.Header.Get("Authorization"), "Bearer ")
		merchantID, err := s.store.MerchantForAPIKey(key)
		if err != nil {
			http.Error(w, "unauthorized", http.StatusUnauthorized)
			return
		}
		ctx := context.WithValue(r.Context(), merchantKey{}, merchantID)
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}
