def test_approle_auth_works(approle_client):
    """Verify that a client authenticated via AppRole can list its own token."""
    assert approle_client.is_authenticated()
    token_info = approle_client.auth.token.lookup_self()
    assert "test-read-policy" in token_info["data"]["policies"]
