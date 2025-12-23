resource "vault_policy" "test_policy" {
  name = "test-read-policy"
  policy = <<-EOT
    path "${var.kv_mount_path}/data/test/*" {
      capabilities = ["read", "list"]
    }
  EOT
}
