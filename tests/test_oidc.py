import pytest
import os
import requests
import hvac


def get_github_oidc_token(audience):
    """
    Fetch the OIDC token from the GitHub Actions environment.
    """
    request_url = os.getenv("ACTIONS_ID_TOKEN_REQUEST_URL")
    request_token = os.getenv("ACTIONS_ID_TOKEN_REQUEST_TOKEN")

    if not request_url or not request_token:
        raise ValueError("GitHub Actions OIDC environment variables not found.")

    response = requests.get(
        request_url,
        headers={"Authorization": f"Bearer {request_token}"},
        params={"audience": audience},
    )
    response.raise_for_status()
    return response.json()["value"]


@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS") != "true",
    reason="OIDC test only runs in GitHub Actions environment",
)
def test_github_oidc_login(tf_outputs):
    """
    Verify that we can authenticate to Vault using GitHub OIDC token.
    """
    vault_addr = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")

    # Fetch oidc token
    # The audience must match what we configured in Vault.
    # We used "https://github.com/narish" in terraform config.
    audience = "https://github.com/nhsy"

    try:
        id_token = get_github_oidc_token(audience)
    except Exception as e:
        pytest.fail(f"Failed to get OIDC token: {e}")

    # Authenticate with Vault
    client = hvac.Client(url=vault_addr)

    role_name = "github-actions"  # Match the role in terraform/auth_oidc.tf

    try:
        login_response = client.auth.jwt.jwt_login(
            role=role_name,
            jwt=id_token,
            path="jwt",  # Match the path in terraform/auth_oidc.tf
        )
    except Exception as e:
        pytest.fail(f"Vault OIDC login failed: {e}")

    assert client.is_authenticated()

    # Verify we have the expected policies
    policies = login_response["auth"]["policies"]
    assert "default" in policies
    assert "readonly" in policies

    # Optional: Verify we can actually read a secret if one exists
    # and we have permissions. But checking authentication is the primary goal here.
