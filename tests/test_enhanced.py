import pytest
import hvac


def test_approle_cannot_write_secret(approle_client, tf_outputs):
    """Verify that AppRole token cannot write to KV paths (Read-only policy)."""
    mount_point = tf_outputs["kv_mount_path"]
    secret_path = tf_outputs["test_secret_path"]

    with pytest.raises(hvac.exceptions.Forbidden):
        approle_client.secrets.kv.v2.create_or_update_secret(
            path=secret_path, mount_point=mount_point, secret=dict(unauthorized="data")
        )


def test_approle_access_denied_to_sys(approle_client):
    """
    Verify AppRole cannot access system-level endpoints or list other auth backends.
    """
    with pytest.raises(hvac.exceptions.Forbidden):
        approle_client.sys.list_auth_methods()


def test_kv_secret_metadata(vault_client, tf_outputs):
    """Verify metadata retrieval for KV v2 secrets."""
    mount_point = tf_outputs["kv_mount_path"]
    secret_path = tf_outputs["test_secret_path"]

    metadata = vault_client.secrets.kv.v2.read_secret_metadata(
        path=secret_path, mount_point=mount_point
    )
    assert "versions" in metadata["data"]
    # 0 means unlimited versions
    assert metadata["data"]["max_versions"] >= 0


def test_approle_token_properties(approle_client):
    """Verify that the AppRole token has the correct renewal and TTL properties."""
    token_info = approle_client.auth.token.lookup_self()
    assert token_info["data"]["renewable"] is True

    # Verify renewal works
    renew_response = approle_client.auth.token.renew_self()
    assert "auth" in renew_response
    assert renew_response["auth"]["client_token"] == approle_client.token


def test_vault_seal_configuration(vault_client):
    """Verify Shamir threshold and seal status configuration."""
    status = vault_client.sys.read_seal_status()
    assert status["sealed"] is False
    assert status["t"] == 3  # Threshold for current setup
    assert status["n"] == 5  # Total shares for current setup
