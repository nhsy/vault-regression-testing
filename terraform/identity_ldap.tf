resource "vault_identity_group" "developers" {
  name     = "developers"
  type     = "external"
  policies = ["read-only"]
}

resource "vault_identity_group_alias" "developers" {
  name           = "developers"
  mount_accessor = vault_ldap_auth_backend.ldap.accessor
  canonical_id   = vault_identity_group.developers.id
}

resource "vault_identity_group" "admins" {
  name     = "vault-admins"
  type     = "external"
  policies = ["admin"]
}

resource "vault_identity_group_alias" "admins" {
  name           = "vault-admins"
  mount_accessor = vault_ldap_auth_backend.ldap.accessor
  canonical_id   = vault_identity_group.admins.id
}
