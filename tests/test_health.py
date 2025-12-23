def test_vault_health(vault_client):
    """Verify Vault is unsealed and healthy."""
    health = vault_client.sys.read_health_status(method="GET")
    assert health["initialized"] is True
    assert health["sealed"] is False


def test_vault_version(vault_client):
    """Verify Vault version starts with 1.19."""
    health = vault_client.sys.read_health_status(method="GET")
    assert health["version"].startswith("1.19")
