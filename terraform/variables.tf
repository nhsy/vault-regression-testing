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
