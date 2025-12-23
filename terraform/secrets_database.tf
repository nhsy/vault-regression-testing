# Database secrets engine mount
resource "vault_mount" "database" {
  path = "database"
  type = "database"
}

# PostgreSQL connection configuration
resource "vault_database_secret_backend_connection" "postgres" {
  backend       = vault_mount.database.path
  name          = "postgres"
  allowed_roles = ["readonly", "readwrite"]

  postgresql {
    connection_url = "postgresql://{{username}}:{{password}}@postgres:5432/vaultdb?sslmode=disable"
    username       = "vaultadmin"
    password       = "vaultadminpassword"
  }
}

# Read-only dynamic role
resource "vault_database_secret_backend_role" "readonly" {
  backend = vault_mount.database.path
  name    = "readonly"
  db_name = vault_database_secret_backend_connection.postgres.name
  creation_statements = [
    "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';",
    "GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";"
  ]
  revocation_statements = [
    "DROP OWNED BY \"{{name}}\";",
    "DROP ROLE IF EXISTS \"{{name}}\";"
  ]
  default_ttl = 300
  max_ttl     = 600
}

# Read-write dynamic role
resource "vault_database_secret_backend_role" "readwrite" {
  backend = vault_mount.database.path
  name    = "readwrite"
  db_name = vault_database_secret_backend_connection.postgres.name
  creation_statements = [
    "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';",
    "GRANT USAGE, CREATE ON SCHEMA public TO \"{{name}}\";",
    "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";"
  ]
  revocation_statements = [
    "DROP OWNED BY \"{{name}}\";",
    "DROP ROLE IF EXISTS \"{{name}}\";"
  ]
  default_ttl = 300
  max_ttl     = 600
}
