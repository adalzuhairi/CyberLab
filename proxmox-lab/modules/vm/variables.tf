variable "name" {
  type = string
}

variable "description" {
  type = string
}

variable "vm_id" {
  type = number
}

variable "node_name" {
  type = string
}

variable "template_id" {
  type = number
}

variable "cpu" {
  type = number
}

variable "memory" {
  type = number
}

variable "disk" {
  type = number
}

variable "bridge" {
  type = string
}

variable "on_boot" {
  type = bool
}

variable "agent" {
  type = bool
}

variable "tags" {
  type = list(string)
}

variable "ci_user" {
  type = string
}

variable "ci_password" {
  type      = string
  sensitive = true
}

variable "ssh_public_key" {
  type = string
}
