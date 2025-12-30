resource "vault_mount" "pki" {
  path        = var.pki_mount_path
  type        = "pki"
  description = "PKI secrets engine for testing"

  default_lease_ttl_seconds = 3600
  max_lease_ttl_seconds     = 86400
}

resource "vault_pki_secret_backend_root_cert" "test_root" {
  depends_on = [vault_mount.pki]

  backend = vault_mount.pki.path

  type                 = "internal"
  common_name          = "example.com"
  ttl                  = "87600h"
  format               = "pem"
  private_key_format   = "der"
  key_type             = "rsa"
  key_bits             = 2048
  exclude_cn_from_sans = true
}

resource "vault_pki_secret_backend_role" "example_dot_com" {
  backend = vault_mount.pki.path
  name    = "example-dot-com"
  ttl     = 3600

  allow_localhost    = true
  allowed_domains    = ["example.com"]
  allow_subdomains   = true
  allow_bare_domains = true
  allow_glob_domains = false
  allow_any_name     = false
  enforce_hostnames  = true
  generate_lease     = true
}
