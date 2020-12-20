package handler

import (
	"context"

	pb "github.com/LaPluses/lutece-next-prototype/proto/api"
)

// GetUser Api implementation
func (WebServer) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.GetUserResponse, error) {
	return &pb.GetUserResponse{User: &pb.User{Role: pb.User_NORMAL, Name: "John"}}, nil
}
