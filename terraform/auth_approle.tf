resource "vault_auth_backend" "approle" {
  type = "approle"
  path = var.approle_mount_path
}

resource "vault_approle_auth_backend_role" "test_role" {
  backend        = vault_auth_backend.approle.path
  role_name      = "test-app-role"
  token_policies = ["default", vault_policy.test_policy.name]
}
