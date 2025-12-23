import hvac
import os


def test_ldap_auth_alice():
    """Test LDAP authentication for user 'alice' (developer)."""
    client = hvac.Client(url=os.getenv("VAULT_ADDR"))

    login_response = client.auth.ldap.login(
        username="alice", password="password", mount_point="ldap"
    )

    assert client.is_authenticated()

    # Alice should have 'read-only' policy via 'developers' group
    token_policies = login_response["auth"]["policies"]
    # Sometimes identity policies are not in the top-level 'policies' list immediately
    # depending on token type, but for default service tokens they usually are.
    # If not, check 'identity_policies'.
    all_policies = token_policies + login_response["auth"].get("identity_policies", [])
    assert "read-only" in all_policies


def test_ldap_auth_bob():
    """Test LDAP authentication for user 'bob' (admin)."""
    client = hvac.Client(url=os.getenv("VAULT_ADDR"))

    login_response = client.auth.ldap.login(
        username="bob", password="password", mount_point="ldap"
    )

    assert client.is_authenticated()
    token_policies = login_response["auth"]["policies"]
    all_policies = token_policies + login_response["auth"].get("identity_policies", [])
    assert "admin" in all_policies


def test_ldap_secrets_static(vault_client):
    """Test fetching static LDAP creds."""
    # Using generic read since specific method might vary
    path = "ldap-secrets/static-cred/charlie-static"

    response = vault_client.read(path)

    assert response is not None
    assert "data" in response
    assert "password" in response["data"]
    assert response["data"]["dn"] == "uid=charlie,ou=People,dc=example,dc=org"


def test_ldap_secrets_dynamic(vault_client):
    """Test generating dynamic LDAP creds."""
    # Using generic read (it's actually a read on creds/role_name)
    path = "ldap-secrets/creds/dynamic-dev"

    response = vault_client.read(path)

    assert response is not None
    assert "data" in response
    username = response["data"]["username"]
    password = response["data"]["password"]

    assert username
    assert password

    # Verify lease
    assert "lease_id" in response
