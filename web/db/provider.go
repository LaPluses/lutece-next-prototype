package db

import (
	"log"

	"github.com/jmoiron/sqlx"

	// Provide sqlite3 driver implmentation
	_ "github.com/mattn/go-sqlite3"
)

// DatabaseType enum type, currently support
type DatabaseType = uint8

const (
	// MYSQL database
	MYSQL DatabaseType = 1
	// SQLITE3 database with in-memory mode, used for testing
	SQLITE3 DatabaseType = 2
)

var (
	db *sqlx.DB = nil
)

// InitializeDatabase used to initliaze the database related, must be called in program entry point
func InitializeDatabase(databaseType DatabaseType, dsn string) {
	var driverName = ""
	switch databaseType {
	case MYSQL:
		log.Fatalf("Still not support mysql database")
	case SQLITE3:
		driverName = "sqlite3"
	default:
		log.Fatalf("Unknown database type")
	}
	db = sqlx.MustConnect(driverName, dsn)
}

// GetDB function interface, call it to get one *sqlx.Db instance
func GetDB() *sqlx.DB {
	if db == nil {
		log.Fatal("Please call InitializeDatabase before accessing it")
	}
	return db
}
