package payments

import "net/http"

type Server struct {
	store *Store
}

func NewServer(store *Store) http.Handler {
	s := &Server{store: store}
	mux := http.NewServeMux()
	return s.requireMerchant(mux)
}
