def test_kv_secret_readable(vault_client, tf_outputs):
    """Verify the test secret created by Terraform is readable."""
    mount_point = tf_outputs["kv_mount_path"]
    secret_path = tf_outputs["test_secret_path"]

    read_response = vault_client.secrets.kv.v2.read_secret_version(
        path=secret_path, mount_point=mount_point, raise_on_deleted_version=True
    )

    assert read_response["data"]["data"]["api_key"] == "test-12345"
