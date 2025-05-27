# Kubernetes(k8s)

## Minikube

- Minimum 4GB ram.
- Its restart (stop/start) process will not save your deployed resources (Pod, Deployment, Service, ConfigMap, etc) by default.

```bash
# Minikube
# Ubuntu 24.04

sudo apt install -y curl wget apt-transport-https

## Download And Install Minikube Binary
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
sudo usermod -aG docker $USER && newgrp docker # or logout/in again

gnome-session-quit --no-prompt # Desktop logout

## Test
docker run hello-world
minikube version

## kubectl
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version -o yaml

## minikube
minikube start --driver=docker
## Start minikube with customize resources
minikube start --addons=ingress --cpus=2 --cni=flannel --install-addons=true --kubernetes-version=stable --memory=4g

minikube status

kubectl cluster-info
kubectl get nodes

## Managing Minikube Addons
minikube addons list
minikube dashboard enable # or minikube addons enable dashboard

mkdir k8s; cd k8s
```

### Practice

#### Nginx

```bash
tee nginx-deployment.yaml > /dev/null <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
EOF

tee nginx-service.yaml > /dev/null <<EOF
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: NodePort
EOF

tee nginx-ingress.yaml > /dev/null <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /nginx
        pathType: Prefix
        backend:
          service:
            name: nginx-service
            port:
              number: 80
EOF

minikube addons enable ingress
kubectl apply -f nginx-deployment.yaml
kubectl apply -f nginx-service.yaml
kubectl apply -f nginx-ingress.yaml
kubectl get pods
kubectl get svc
kubectl get ingress
minikube ip
```

```bash
# Deploy nginx based deployment
kubectl create deployment my-app --image=nginx

# Verify deployment status
kubectl get deployments.apps my-app
kubectl get pods

## Expose the deployment
kubectl expose deployment my-app --name=my-app-svc --type=NodePort --port=80
kubectl get svc my-app-svc

kubectl patch svc ingress-nginx-controller -n ingress-nginx -p '{"spec": {"type": "LoadBalancer"}}'
minikube tunnel

##  Get service url
URL=$(minikube service my-app-svc --url)
curl $URL

minikube stop
minikube config set cpus 4
minikube config set memory 8192
minikube delete
minikube start

# Other

sudo minikube start --driver=none

## Exiting due to GUEST_MISSING_CONNTRACK: Sorry, Kubernetes 1.32.0 requires conntrack to be installed in root's path
sudo apt-get install -y conntrack
sudo ln -s /usr/sbin/conntrack conntrack /usr/bin/conntrack

## Exiting due to GUEST_MISSING_CONNTRACK: Sorry, Kubernetes 1.32.0 requires crictl to be installed in root's path
CRICTL_VERSION="v1.33.0"
wget https://github.com/kubernetes-sigs/cri-tools/releases/download/$CRICTL_VERSION/crictl-$CRICTL_VERSION-linux-amd64.tar.gz
sudo tar zxvf crictl-$CRICTL_VERSION-linux-amd64.tar.gz -C /usr/local/bin
rm -f crictl-$CRICTL_VERSION-linux-amd64.tar.gz

## Please install cri-dockerd
curl -LO https://github.com/Mirantis/cri-dockerd/releases/download/v0.3.17/cri-dockerd_0.3.17.3-0.debian-bookworm_amd64.deb; sudo dpkg -i cri-dockerd_0.3.17.3-0.debian-bookworm_amd64.deb

## Please install containernetworking-plugins
sudo apt install -y containernetworking-plugins
wget https://github.com/containernetworking/plugins/releases/download/v1.6.2/cni-plugins-linux-amd64-v1.6.2.tgz
sudo mkdir -p /opt/cni/bin
sudo tar -C /opt/cni/bin -xzvf cni-plugins-linux-amd64-v1.6.2.tgz
sudo mkdir -p /etc/cni/net.d

# Microservice for fetching the latest posts of Medium.
kubectl create deployment medium-api \
  --image=evenchange4/micro-medium-api:latest \
  --port=3000
kubectl get deployments # default
kubectl get pods -o wide

kubectl expose deployment medium-api --type=LoadBalancer
kubectl get service
minikube service medium-api

kubectl scale deployment/medium-api --replicas=2
kubectl get pods -o wide

kubectl get deployment medium-api -o yaml

# Ack
template:
    spec:
      containers:
      - name: micro-medium-api

kubectl set image deployments/medium-api \
micro-medium-api=evenchange4/micro-medium-api:2.1.0
kubectl rollout status deployments/medium-api
# Logs
kubectl logs --follow deployments/medium-api
# Execute Commands
kubectl exec deployments/medium-api -it -- ls

# Kill
kubectl delete service medium-api
kubectl delete deployment medium-api
minikube stop

# Oh-my-zsh Autocompletion Plugin
sudo apt install -y zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
vi ~/.zshrc
# plugins=(git) to plugins=(git kubectl)

kubectl get services medium-api -o yaml > ./service.yaml
kubectl create -f ./service.yaml

kubectl get deployments --all-namespaces

kubectl delete deployments medium-api
kubectl delete pod medium-api

# Helm v3

wget https://get.helm.sh/helm-v3.17.0-linux-amd64.tar.gz
tar -xvf helm-v3.17.0-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin
helm version
helm init

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install my-wordpress-new bitnami/wordpress
kubectl get svc --namespace default -w my-wordpress
kubectl get services

helm install my-release \
  --set wordpressUsername=admin \
  bitnami/wordpress

helm install \
  my-release \
  -f values.yaml \
  stable/wordpress

helm create mcs-lite-chart
cd mcs-lite-chart
helm install --dry-run --debug . my-mcs-lite-chart
helm install mcs-lite-chart .

helm ls
helm upgrade mcs-lite-app .
helm rollback mcs-lite-app 1
helm install ./charts/mcs-lite-chart-0.1.0.tgz
```

