 This section describes how to deploy your application using Kubernetes manifests and provides detailed explanations for each file.

---

## Kubernetes Deployment for Recipe Management System

This section describes the Kubernetes manifests and configurations used to deploy the Recipe Management System on a Kubernetes cluster. The setup includes the creation of a namespace, the deployment of MySQL, and the deployment of the producer and consumer services.

### Table of Contents

1. [Namespaces](#namespaces)
2. [MySQL](#mysql)
3. [Producer](#producer)
4. [Consumer Services](#consumer-services)
5. [How to Apply the Manifests](#how-to-apply-the-manifests)
6. [Example Commands](#example-commands)

---

### Namespaces

**`my-namespace.yaml`**

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-namespace
```

This manifest creates a namespace named `my-namespace` for organizing the Kubernetes resources.

### MySQL

**`mysql-storage.yaml`**

**`mysql-pvc.yaml`**

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
  namespace: my-namespace
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi  # Adjust size as per your requirements
```

This manifest creates a PersistentVolumeClaim (PVC) for MySQL, which requests 1Gi of storage.

**`mysql-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
  namespace: my-namespace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:5.7
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "pesuims"
        ports:
        - containerPort: 3309
          name: mysql
        volumeMounts:
        - name: mysql-persistent-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-persistent-storage
        persistentVolumeClaim:
          claimName: mysql-pvc
```

This manifest deploys a MySQL container with a root password set to `pesuims` and mounts the PVC for persistent storage.

**`mysql-secret.yaml`**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secret
  namespace: my-namespace
type: Opaque
data:
  MYSQL_ROOT_PASSWORD: cGVzdWltcw==  # Base64 encoded 'pesuims'
```

This manifest creates a secret for storing the MySQL root password.

**`mysql-service.yaml`**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
  namespace: my-namespace
spec:
  selector:
    app: mysql
  ports:
    - protocol: TCP
      port: 3306
      targetPort: 3306
  type: ClusterIP
```

This manifest exposes the MySQL service on port `3306` within the cluster.

### Producer

**`producer-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: producer-deployment
  namespace: my-namespace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: producer
  template:
    metadata:
      labels:
        app: producer
    spec:
      containers:
        - name: producer
          image: bharathoptdocker/python-producer:1
          ports:
            - containerPort: 5000
```

This manifest deploys the producer service, which is responsible for sending messages to RabbitMQ and providing API endpoints.

**`producer-service.yaml`**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: producer-service
  namespace: my-namespace
spec:
  selector:
    app: producer
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: ClusterIP
```

This manifest exposes the producer service on port `80` within the cluster.

### Consumer Services

Each consumer service has a similar deployment and service configuration:

#### **Consumer One**

**`consumer-one-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: consumer-one-deployment
  namespace: my-namespace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: consumer-one
  template:
    metadata:
      labels:
        app: consumer-one
    spec:
      containers:
        - name: consumer-one
          image: bharathoptdocker/python-consumer-one
          ports:
            - containerPort: 5000
```

**`consumer-one-service.yaml`**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: consumer-one-service
  namespace: my-namespace
spec:
  selector:
    app: consumer-one
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: ClusterIP
```

#### **Consumer Two**

**`consumer-two-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: consumer-two-deployment
  namespace: my-namespace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: consumer-two
  template:
    metadata:
      labels:
        app: consumer-two
    spec:
      containers:
        - name: consumer-two
          image: bharathoptdocker/python-consumer-two:1
          ports:
            - containerPort: 5000
```

**`consumer-two-service.yaml`**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: consumer-two-service
  namespace: my-namespace
spec:
  selector:
    app: consumer-two
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: ClusterIP
```

#### **Consumer Three**

**`consumer-three-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: consumer-three-deployment
  namespace: my-namespace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: consumer-three
  template:
    metadata:
      labels:
        app: consumer-three
    spec:
      containers:
        - name: consumer-three
          image: bharathoptdocker/python-consumer-three:1
          ports:
            - containerPort: 5000
```

**`consumer-three-service.yaml`**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: consumer-three-service
  namespace: my-namespace
spec:
  selector:
    app: consumer-three
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: ClusterIP
```

#### **Consumer Four**

**`consumer-four-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: consumer-four-deployment
  namespace: my-namespace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: consumer-four
  template:
    metadata:
      labels:
        app: consumer-four
    spec:
      containers:
        - name: consumer-four
          image: bharathoptdocker/python-consumer-four:1
          ports:
            - containerPort: 5000
```

**`consumer-four-service.yaml`**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: consumer-four-service
  namespace: my-namespace
spec:
  selector:
    app: consumer-four
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: ClusterIP
```

### How to Apply the Manifests

To deploy the application, follow these steps:

1. **Apply the Namespace:**

    ```bash
    kubectl apply -f kubernetes/manifest/my-namespace.yaml
    ```

2. **Deploy MySQL:**

    ```bash
    kubectl apply -f kubernetes/manifest/mysql-storage.yaml
    kubectl apply -f kubernetes/manifest/mysql-secret.yaml
    kubectl apply -f kubernetes/manifest/mysql-deployment.yaml
    kubectl apply -f kubernetes/manifest/mysql-service.yaml
    ```

3. **Deploy Producer:**

    ```bash
    kubectl apply -f kubernetes/manifest/producer/producer-deployment.yaml
    kubectl apply -f kubernetes/manifest/producer/producer-service.yaml
    ```

4. **Deploy Consumer Services:**

    ```bash
    kubectl apply -f kubernetes/manifest/consumer_one/deployment.yaml
    kubectl apply -f kubernetes/manifest/consumer_one/service.yaml

    kubectl apply -f kubernetes/manifest/consumer_two/deployment.yaml
    kubectl apply -f kubernetes/manifest/consumer_two/service.yaml

    kubectl apply -f kubernetes/manifest/consumer_three/deployment.yaml
    kubectl apply -f kubernetes/manifest/consumer_three/service.yaml

    kub

ectl apply -f kubernetes/manifest/consumer_four/deployment.yaml
    kubectl apply -f kubernetes/manifest/consumer_four/service.yaml
    ```

### Example Commands

Here are some example commands you might use during deployment:

```bash
# Check the status of the namespace
kubectl get namespaces

# Check the status of MySQL Pods
kubectl get pods -n my-namespace -l app=mysql

# Check the status of the Producer Pods
kubectl get pods -n my-namespace -l app=producer

# Check the status of Consumer One Pods
kubectl get pods -n my-namespace -l app=consumer-one

# Check the status of all services in the namespace
kubectl get services -n my-namespace
```

---

This section provides the necessary Kubernetes manifests for deploying the Recipe Management System and instructions on how to apply these manifests to set up the environment.
