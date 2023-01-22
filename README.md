# aperture

A demo of several web and infrastructure tools, mainly using python for web
services, kubernetes/helm/terraform for infrastructure, and [localstack] for
emulating AWS services. A sort of "home lab" for playing with kubernetes etc.

(Yes, the infrastructure is way overkill given what the applications are; it's
meant as a demo.)

(localstack components TODO)

Named lovingly after [Aperture Science][].

## Requirements

- [kubectl][]
- [k3d][]
- [terraform][]

## Setup

To create the cluster locally (all from root directory):
```
export KUBECONFIG=$(realpath ./config/kubeconfig)
k3d cluster create aperture
terraform -chdir=tf-local init
terraform -chdir=tf-local plan -out plan
terraform -chdir=tf-local apply plan
```

Build images:
```
docker build -t conway services/conway
k3d image import --cluster aperture conway
```

Deploy kubernetes resources:
```
kubectl apply -f k8s/services/conway/conway-service.yaml
kubectl apply -f k8s/services/conway/conway-deploy.yaml
```

## Services

### Conway

Simple game of life implementation based on the rust wasm tutorial.


[Aperture Science]: https://theportalwiki.com/wiki/Aperture_Science
[kubectl]: https://kubernetes.io/docs/tasks/tools/
[k3d]: https://k3d.io/v5.4.6/
[localstack]: https://localstack.cloud/
[terraform]: https://www.terraform.io/
