# Podman

## Quick

```bash
podman pull docker.io/hello-world
podman pull docker.io/nginx

podman images

podman run --name hello docker.io/hello-world
podman run -d --name hello docker.io/hello-world
podman run -d -p 8040:80 --name nginx docker.io/nginx

podman stop nginx

# Auto remove container
podman run --rm --name hello docker.io/hello-world
podman rm hello
podman rm --force nginx

podman kube generate hello > hello.yaml
podman kube generate nginx > nginx.yaml

kubectl apply -f hello.yaml
kubectl apply -f nginx.yaml

kubectl get pods
kubectl get pods -A
kubectl logs hello-pod
kubectl delete pod hello-pod
```

## Troubleshooting

Error at Windows:

API forwarding for Docker API clients is not available due to the following startup failures.
        CreateFile \\.\pipe\podman-machine-default: All pipe instances are busy.

1. Stop Docker
2. Open Power Shell with Administrator
3. Run `wsl --update`

