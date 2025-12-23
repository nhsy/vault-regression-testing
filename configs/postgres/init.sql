-- PostgreSQL initialization script for Vault dynamic database secrets
-- This script grants the necessary permissions for Vault to manage dynamic roles

-- Grant Vault user ability to create and manage roles
GRANT ALL PRIVILEGES ON DATABASE vaultdb TO vaultadmin;
GRANT ALL PRIVILEGES ON SCHEMA public TO vaultadmin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO vaultadmin;

-- Grant USAGE on public schema to all users (required for PostgreSQL 15+)
-- Note: We do NOT grant CREATE to PUBLIC - only specific roles will get that
GRANT USAGE ON SCHEMA public TO PUBLIC;

-- Create a test table for verification
CREATE TABLE IF NOT EXISTS test_data (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO test_data (message) VALUES ('Sample data for testing read permissions');
