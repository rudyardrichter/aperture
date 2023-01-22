terraform {
  required_version = "~> 1.3"

  required_providers {
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.8"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.16"
    }
  }
}

provider "kubernetes" {
  config_context = var.k8s_config_context
  config_path    = var.k8s_config_path
}

resource "kubernetes_namespace" "aperture_namespace" {
  metadata {
    name = "ns-aperture"
  }
}

provider "helm" {
  kubernetes {
    config_context = var.k8s_config_context
    config_path    = var.k8s_config_path
  }
}
