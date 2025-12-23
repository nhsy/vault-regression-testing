resource "vault_ldap_auth_backend" "ldap" {
  path         = "ldap"
  url          = var.ldap_url
  userdn       = var.ldap_user_dn
  userattr     = "uid"
  groupdn      = var.ldap_group_dn
  groupattr    = "cn"
  binddn       = var.ldap_bind_dn
  bindpass     = var.ldap_bind_password
  insecure_tls = true
}