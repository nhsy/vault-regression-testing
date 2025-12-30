resource "vault_jwt_auth_backend" "github_actions" {
  description        = "OIDC backend for GitHub Actions"
  path               = "jwt"
  oidc_discovery_url = "https://token.actions.githubusercontent.com"
  bound_issuer       = "https://token.actions.githubusercontent.com"
}

resource "vault_jwt_auth_backend_role" "github_actions" {
  backend   = vault_jwt_auth_backend.github_actions.path
  role_name = "github-actions"

  bound_audiences = ["https://github.com/${var.github_org}/${var.github_repository}"]

  user_claim = "repository"

  bound_claims = {
    repository = "${var.github_org}/${var.github_repository}"
  }

  role_type      = "jwt"
  token_policies = ["default", "read-only"]
  token_ttl      = 3600
}
