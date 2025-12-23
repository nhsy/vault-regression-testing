output "vault_address" {
  value = var.vault_address
}

output "kv_mount_path" {
  value = vault_mount.kv.path
}

output "approle_mount_point" {
  value = vault_auth_backend.approle.path
}

output "approle_role_name" {
  value = vault_approle_auth_backend_role.test_role.role_name
}

output "approle_role_id" {
  value     = vault_approle_auth_backend_role.test_role.role_id
  sensitive = true
}

output "test_secret_path" {
  value = vault_kv_secret_v2.test_secret.name
}

output "test_config" {
  value = {
    vault_address      = var.vault_address
    kv_mount           = vault_mount.kv.path
    approle_mount      = vault_auth_backend.approle.path
    approle_role       = vault_approle_auth_backend_role.test_role.role_name
    test_secret_path   = vault_kv_secret_v2.test_secret.name
    test_policy        = vault_policy.test_policy.name
  }
}
