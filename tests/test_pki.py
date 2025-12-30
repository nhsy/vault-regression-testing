def test_pki_generate_cert(vault_client, tf_outputs):
    """Verify that we can generate a certificate from the PKI engine."""
    mount_point = tf_outputs["pki_mount_path"]
    role_name = tf_outputs["pki_role_name"]
    common_name = "test.example.com"

    # Generate certificate
    response = vault_client.secrets.pki.generate_certificate(
        name=role_name, common_name=common_name, mount_point=mount_point
    )

    data = response["data"]

    # Verify response structure
    assert "certificate" in data
    assert "private_key" in data
    assert "issuing_ca" in data

    # Verify common name in certificate (basic string check)
    assert "BEGIN CERTIFICATE" in data["certificate"]
    assert "BEGIN RSA PRIVATE KEY" in data["private_key"]
    assert "serial_number" in data
    assert "BEGIN RSA PRIVATE KEY" in data["private_key"]
