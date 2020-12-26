package main

import (
	"flag"
	"fmt"
	"log"
	"net"

	db "github.com/LaPluses/lutece-next-prototype/db"
	pb "github.com/LaPluses/lutece-next-prototype/proto/api"

	"github.com/LaPluses/lutece-next-prototype/handler"

	"google.golang.org/grpc"
)

const (
	sqliteDefaultDsn = "file:dist/test.db?cache=shared"
)

var (
	port     = flag.Int("port", 10000, "The server port")
	isSqlite = flag.Bool("sqlite", false, "Using sqlite3 database")
	isMysql  = flag.Bool("mysql", false, "Using mysql database")
	dsn      = flag.String("dsn", "", "The datasource string for db configuration")
)

func getDsnString() string {
	if len(*dsn) > 0 {
		return *dsn
	} else if *isSqlite {
		return sqliteDefaultDsn
	} else if *isMysql {
		log.Fatalf("Mysql still not supported yet")
	}
	log.Fatalf("Failed to get DSN string")
	return ""
}

func main() {
	// Flag parsing
	flag.Parse()
	// Database initialization
	if *isSqlite {
		db.InitializeDatabase(db.SQLITE3, getDsnString())
	} else {
		db.InitializeDatabase(db.MYSQL, getDsnString())
	}
	// gRPC server serving
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
