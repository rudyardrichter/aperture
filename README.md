# aperture

A demo of several web and infrastructure tools, using an assortment of web
service tools, kubernetes/helm/terraform for infrastructure, and [localstack]
for emulating AWS services. A sort of "home lab" for playing with kubernetes
etc.

(Yes, the infrastructure is way overkill given what the applications are; it's
meant as a demo.)

(localstack components TODO)

Named lovingly after [Aperture Science][].

## Requirements

- [docker][]
- [docker-compose][] to build all the images at once
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

Build images and import them into k3d:
```bash
docker compose build
k3d image import --cluster aperture conway dict-regex
```

Deploy kubernetes resources:
```bash
declare -a services=("conway" "dict-regex")
for service in "${services[@]}"; do
    kubectl apply -f "k8s/services/${service}/${service}-service.yaml"
    kubectl apply -f "k8s/services/${service}/${service}-deploy.yaml"
done
```

## Services

### conway

Simple game of life implementation based on the rust wasm tutorial.

### dict-regex

A tiny dictionary lookup service; serves an endpoint which accepts a regex to
match words against.


[Aperture Science]: https://theportalwiki.com/wiki/Aperture_Science
[docker]: https://docs.docker.com/get-docker/
[docker-compose]: https://docs.docker.com/compose/install/
[kubectl]: https://kubernetes.io/docs/tasks/tools/
[k3d]: https://k3d.io/v5.4.6/
[localstack]: https://localstack.cloud/
[terraform]: https://www.terraform.io/
