locals {

  vms = {

    ubuntu01 = {
      name        = "ubuntu-lab01"
      description = "Ubuntu Server 24.04"

      vmid        = 201
      template_id = 9000

      cpu    = 2
      memory = 2048
      disk   = 20

      bridge = "vmbr0"

      on_boot = true
      agent   = true

      tags = [
        "ubuntu",
        "lab"
      ]
    }

    ubuntu02 = {
      name        = "ubuntu-lab02"
      description = "Deuxième serveur Ubuntu"

      vmid        = 202
      template_id = 9000

      cpu    = 2
      memory = 4096
      disk   = 40

      bridge = "vmbr0"

      on_boot = true
      agent   = true

      tags = [
        "ubuntu",
        "docker"
      ]
    }

  }

}

module "vm" {

  source = "./modules/vm"

  for_each = local.vms

  name        = each.value.name
  description = each.value.description

  vm_id     = each.value.vmid
  node_name = "pve"

  template_id = each.value.template_id

  cpu    = each.value.cpu
  memory = each.value.memory
  disk   = each.value.disk

  bridge = each.value.bridge

  on_boot = each.value.on_boot
  agent   = each.value.agent

  tags = each.value.tags

  ci_user        = var.ci_user
  ci_password    = var.ci_password
  ssh_public_key = var.ssh_public_key
}

output "vms" {

  value = {
    for name, vm in module.vm :
    name => {
      id   = vm.vm_id
      name = vm.vm_name
    }
  }

}
