resource "proxmox_virtual_environment_vm" "this" {

  name        = var.name
  description = var.description

  node_name = var.node_name
  vm_id     = var.vm_id

  on_boot = var.on_boot

  tags = var.tags

  clone {
    vm_id = var.template_id
    full  = true
  }

  agent {
    enabled = var.agent
  }

  cpu {
    cores = var.cpu
    type  = "qemu64"
  }

  memory {
    dedicated = var.memory
  }

  disk {
    datastore_id = "local-lvm"
    interface    = "scsi0"
    size         = var.disk
  }

  network_device {
    bridge = var.bridge
  }

  initialization {

    user_account {
      username = var.ci_user
      password = var.ci_password

      keys = [
        var.ssh_public_key
      ]
    }

    ip_config {
      ipv4 {
        address = "dhcp"
      }
    }
  }
}
