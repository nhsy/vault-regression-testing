import pytest
import psycopg2
import time


def test_database_mount_accessible(vault_client, tf_outputs):
    """Verify database secrets engine is mounted."""
    mounts = vault_client.sys.list_mounted_secrets_engines()
    assert "database/" in mounts
    assert mounts["database/"]["type"] == "database"


def test_database_connection_configured(vault_client, tf_outputs):
    """Verify PostgreSQL connection is configured."""
    database_mount = tf_outputs["database_mount_path"]
    response = vault_client.read(f"{database_mount}/config/postgres")
    assert response is not None
    assert response["data"]["plugin_name"] == "postgresql-database-plugin"


def test_generate_readonly_credentials(vault_client, tf_outputs):
    """Generate and verify read-only dynamic credentials."""
    database_mount = tf_outputs["database_mount_path"]
    readonly_role = tf_outputs["database_roles"]["readonly"]

    # Request credentials
    response = vault_client.secrets.database.generate_credentials(
        name=readonly_role, mount_point=database_mount
    )

    username = response["data"]["username"]
    password = response["data"]["password"]
    lease_id = response["lease_id"]

    assert username is not None
    assert password is not None
    assert lease_id is not None

    # Verify credentials work
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="vaultdb",
        user=username,
        password=password,
    )
    cursor = conn.cursor()

    # Verify read access on existing table
    cursor.execute("SELECT COUNT(*) FROM test_data")
    count = cursor.fetchone()[0]
    assert count >= 1

    # Verify no write access
    with pytest.raises(psycopg2.errors.InsufficientPrivilege):
        cursor.execute("CREATE TABLE test_table (id INT)")

    cursor.close()
    conn.close()

    # Clean up lease
    vault_client.sys.revoke_lease(lease_id)


def test_generate_readwrite_credentials(vault_client, tf_outputs):
    """Generate and verify read-write dynamic credentials."""
    database_mount = tf_outputs["database_mount_path"]
    readwrite_role = tf_outputs["database_roles"]["readwrite"]

    # Request credentials
    response = vault_client.secrets.database.generate_credentials(
        name=readwrite_role, mount_point=database_mount
    )

    username = response["data"]["username"]
    password = response["data"]["password"]
    lease_id = response["lease_id"]

    # Verify credentials work with write access
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="vaultdb",
        user=username,
        password=password,
    )
    cursor = conn.cursor()

    # Verify write access
    cursor.execute("CREATE TABLE test_table (id INT)")
    cursor.execute("INSERT INTO test_table VALUES (1)")
    cursor.execute("SELECT * FROM test_table")
    result = cursor.fetchone()
    assert result[0] == 1

    # Cleanup table
    cursor.execute("DROP TABLE test_table")
    conn.commit()
    cursor.close()
    conn.close()

    # Clean up lease
    vault_client.sys.revoke_lease(lease_id)


def test_credential_revocation(vault_client, tf_outputs):
    """Verify credentials are revoked properly."""
    database_mount = tf_outputs["database_mount_path"]
    readonly_role = tf_outputs["database_roles"]["readonly"]

    # Request credentials
    response = vault_client.secrets.database.generate_credentials(
        name=readonly_role, mount_point=database_mount
    )

    username = response["data"]["username"]
    password = response["data"]["password"]
    lease_id = response["lease_id"]

    # Verify credentials work
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="vaultdb",
        user=username,
        password=password,
    )
    conn.close()

    # Revoke lease
    vault_client.sys.revoke_lease(lease_id)

    # Wait for revocation to take effect
    time.sleep(2)

    # Verify credentials no longer work
    with pytest.raises(psycopg2.OperationalError):
        psycopg2.connect(
            host="localhost",
            port=5432,
            database="vaultdb",
            user=username,
            password=password,
        )


def test_multiple_credentials_independent(vault_client, tf_outputs):
    """Verify multiple credentials can be generated and work independently."""
    database_mount = tf_outputs["database_mount_path"]
    readonly_role = tf_outputs["database_roles"]["readonly"]

    # Generate first credential
    response1 = vault_client.secrets.database.generate_credentials(
        name=readonly_role, mount_point=database_mount
    )
    username1 = response1["data"]["username"]
    password1 = response1["data"]["password"]
    lease_id1 = response1["lease_id"]

    # Generate second credential
    response2 = vault_client.secrets.database.generate_credentials(
        name=readonly_role, mount_point=database_mount
    )
    username2 = response2["data"]["username"]
    password2 = response2["data"]["password"]
    lease_id2 = response2["lease_id"]

    # Verify both credentials are different
    assert username1 != username2
    assert password1 != password2
    assert lease_id1 != lease_id2

    # Verify both credentials work
    conn1 = psycopg2.connect(
        host="localhost",
        port=5432,
        database="vaultdb",
        user=username1,
        password=password1,
    )
    conn2 = psycopg2.connect(
        host="localhost",
        port=5432,
        database="vaultdb",
        user=username2,
        password=password2,
    )

    conn1.close()
    conn2.close()

    # Cleanup
    vault_client.sys.revoke_lease(lease_id1)
    vault_client.sys.revoke_lease(lease_id2)


def test_credential_ttl_within_limits(vault_client, tf_outputs):
    """Verify credential TTL is within configured limits."""
    database_mount = tf_outputs["database_mount_path"]
    readonly_role = tf_outputs["database_roles"]["readonly"]

    # Request credentials
    response = vault_client.secrets.database.generate_credentials(
        name=readonly_role, mount_point=database_mount
    )

    lease_duration = response["lease_duration"]
    lease_id = response["lease_id"]

    # Verify TTL is within expected range (default_ttl=300, max_ttl=600)
    assert lease_duration <= 600
    assert lease_duration > 0

    # Cleanup
    vault_client.sys.revoke_lease(lease_id)
