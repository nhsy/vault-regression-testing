resource "vault_audit" "stdout" {
  type = "file"
  path = "stdout"
  description = "Audit log to stdout"
  
  options = {
    file_path = "stdout"
    log_raw   = "false"
  }
}
