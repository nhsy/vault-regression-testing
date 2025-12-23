import os


def test_vault_health(vault_client):
    """Verify Vault is unsealed and healthy."""
    health = vault_client.sys.read_health_status(method="GET")
    assert health["initialized"] is True
    assert health["sealed"] is False


def test_vault_version(vault_client):
    """Verify Vault version matches expected version."""
    version = os.getenv("VAULT_VERSION")
    upgrade_version = os.getenv("VAULT_VERSION_UPGRADE")

    health = vault_client.sys.read_health_status(method="GET")
    actual_version = health["version"]

    expected_versions = [v for v in [version, upgrade_version] if v]
    if not expected_versions:
        expected_versions = ["1.19"]

    assert any(actual_version.startswith(v) for v in expected_versions)
