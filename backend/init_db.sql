-- Run this script to initialize the MySQL database
-- Usage: mysql -u root -p < init_db.sql

CREATE DATABASE IF NOT EXISTS yelp_db;
USE yelp_db;

-- Tables are auto-created by SQLAlchemy on first run.
-- This script just ensures the database exists.

SELECT 'Database yelp_db created successfully!' AS status;
