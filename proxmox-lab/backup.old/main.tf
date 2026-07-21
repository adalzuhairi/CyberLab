module "ubuntu_lab01" {

  source = "./modules/vm"

  name        = "ubuntu-lab01"
  vm_id       = 201
  node_name   = "pve"
  template_id = 9000

}
