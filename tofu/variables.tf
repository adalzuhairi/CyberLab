variable "proxmox_endpoint" {
  description = "URL de l'API Proxmox"
  type        = string
}

variable "proxmox_api_token" {
  description = "Token API Proxmox"
  type        = string
  sensitive   = true
}
