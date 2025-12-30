resource "vault_jwt_auth_backend" "github_actions" {
  description        = "OIDC backend for GitHub Actions"
  path               = "jwt"
  oidc_discovery_url = "https://token.actions.githubusercontent.com"
  bound_issuer       = "https://token.actions.githubusercontent.com"
}

resource "vault_jwt_auth_backend_role" "github_actions" {
  backend   = vault_jwt_auth_backend.github_actions.path
  role_name = "github-actions"

  # Validate the token audience.
  # For GitHub Actions, the audience defaults to the repository owner/URL if not customized in the workflow.
  # However, common practice is to rely on bound claims for the specific repo.
  # "sts.amazonaws.com" is a common default audience in GHA for AWS, but for Vault we can match what GHA sends.
  # We will use the generic approach of verifying the claims against our configured variables.
  bound_audiences = ["https://github.com/${var.github_org}"]

  user_claim = "repository"

  bound_claims = {
    repository = "${var.github_org}/${var.github_repository}"
  }

  role_type      = "jwt"
  token_policies = ["default", "readonly"]
  token_ttl      = 3600
}
