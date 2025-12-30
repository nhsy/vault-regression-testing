variable "vault_address" {
  description = "Vault server URL"
  type        = string
  default     = "http://127.0.0.1:8200"
}


variable "kv_mount_path" {
  description = "Path to mount the KV secrets engine"
  type        = string
  default     = "test-kv"
}

variable "approle_mount_path" {
  description = "Path to mount the AppRole auth method"
  type        = string
  default     = "approle"
}

variable "ldap_url" {
  description = "LDAP server URL"
  type        = string
  default     = "ldap://ldap:389"
}

variable "ldap_bind_dn" {
  description = "LDAP Bind DN"
  type        = string
  default     = "cn=admin,dc=example,dc=org"
}

variable "ldap_bind_password" {
  description = "LDAP Bind Password"
  type        = string
  default     = "adminpassword"
}

variable "ldap_user_dn" {
  description = "LDAP User DN"
  type        = string
  default     = "ou=People,dc=example,dc=org"
}

variable "ldap_group_dn" {
  description = "LDAP Group DN"
  type        = string
  default     = "ou=Groups,dc=example,dc=org"
}

variable "pki_mount_path" {
  description = "Path to mount the PKI secrets engine"
  type        = string
  default     = "pki"
}