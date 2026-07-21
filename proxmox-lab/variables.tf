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

variable "ci_user" {
  description = "Utilisateur Cloud-Init"
  type        = string
}

variable "ci_password" {
  description = "Mot de passe Cloud-Init"
  type        = string
  sensitive   = true
}

variable "ssh_public_key" {
  description = "Clé publique SSH"
  type        = string
}
