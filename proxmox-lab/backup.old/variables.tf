variable "proxmox_endpoint" {
  description = "URL de l'API Proxmox"
  type        = string
}

variable "proxmox_api_token_id" {
  description = "Token ID Proxmox"
  type        = string
}

variable "proxmox_api_token_secret" {
  description = "Secret du token Proxmox"
  type        = string
  sensitive   = true
}
