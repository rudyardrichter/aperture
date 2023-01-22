variable "k8s_config_context" {
  type    = string
  default = "k3d-aperture"
}

variable "k8s_config_path" {
  type    = string
  default = "../config/kubeconfig"
}
