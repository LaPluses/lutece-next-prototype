package main

import (
	"flag"
	"fmt"
	"log"
	"net"

	pb "github.com/LaPluses/lutece-next-prototype/proto/api"

	"github.com/LaPluses/lutece-next-prototype/handler"

	"google.golang.org/grpc"
)

var (
	port = flag.Int("port", 10000, "The server port")
)

func main() {
	flag.Parse()
	lis, err := net.Listen("tcp", fmt.Sprintf("localhost:%d", *port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	log.Printf("server listen to :%d\n", *port)
	var opts []grpc.ServerOption
	grpcServer := grpc.NewServer(opts...)
	pb.RegisterWebServer(grpcServer, handler.NewServer())
	grpcServer.Serve(lis)
}
