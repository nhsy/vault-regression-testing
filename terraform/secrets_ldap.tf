resource "vault_ldap_secret_backend" "config" {
  path        = "ldap-secrets"
  binddn      = var.ldap_bind_dn
  bindpass    = var.ldap_bind_password
  url         = var.ldap_url
  userdn      = var.ldap_user_dn
  insecure_tls = true
}

resource "vault_ldap_secret_backend_static_role" "charlie" {
  mount           = vault_ldap_secret_backend.config.path
  role_name       = "charlie-static"
  username        = "charlie"
  dn              = "uid=charlie,ou=People,dc=example,dc=org"
  rotation_period = 86400
}

resource "vault_ldap_secret_backend_dynamic_role" "dynamic" {
  mount         = vault_ldap_secret_backend.config.path
  role_name     = "dynamic-dev"
  creation_ldif = <<EOT
dn: uid={{.Username}},ou=People,dc=example,dc=org
objectClass: inetOrgPerson
objectClass: top
uid: {{.Username}}
cn: {{.Username}}
sn: {{.Username}}
userPassword: {{.Password}}
EOT
  deletion_ldif = <<EOT
dn: uid={{.Username}},ou=People,dc=example,dc=org
changetype: delete
EOT
  rollback_ldif = <<EOT
dn: uid={{.Username}},ou=People,dc=example,dc=org
changetype: delete
EOT
}
