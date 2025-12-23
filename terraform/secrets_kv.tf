resource "vault_mount" "kv" {
  path        = var.kv_mount_path
  type        = "kv"
  options     = { version = "2" }
  description = "KV v2 for testing"
}

resource "vault_kv_secret_v2" "test_secret" {
  mount = vault_mount.kv.path
  name  = "test/app/config"
  data_json = jsonencode({
    api_key = "test-12345"
    debug   = "true"
  })
}
