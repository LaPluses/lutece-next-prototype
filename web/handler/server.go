package handler

import (
	pb "github.com/LaPluses/lutece-next-prototype/proto/api"
)

// WebServer defination
type WebServer struct {
	pb.UnimplementedWebServer
}

// NewServer used to return a new WebServer instance
func NewServer() *WebServer {
	return &WebServer{}
}
