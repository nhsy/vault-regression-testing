resource "vault_policy" "test_policy" {
  name = "test-read-policy"
  policy = <<-EOT
    path "${var.kv_mount_path}/data/test/*" {
      capabilities = ["read", "list"]
    }
  EOT
}

resource "vault_policy" "admin" {
  name = "admin"
  policy = <<-EOT
    path "*" {
      capabilities = ["create", "read", "update", "delete", "list", "sudo"]
    }
  EOT
}

resource "vault_policy" "read_only" {
  name = "read-only"
  policy = <<-EOT
    path "*" {
      capabilities = ["read", "list"]
    }
  EOT
}