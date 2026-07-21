output "vm_id" {
  description = "ID de la machine virtuelle"
  value       = proxmox_virtual_environment_vm.this.vm_id
}

output "vm_name" {
  description = "Nom de la machine virtuelle"
  value       = proxmox_virtual_environment_vm.this.name
}
