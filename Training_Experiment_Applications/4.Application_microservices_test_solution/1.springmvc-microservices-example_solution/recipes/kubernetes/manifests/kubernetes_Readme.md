---
# Spring Boot and MySQL Kubernetes Deployment

This repository contains Kubernetes manifests for deploying a Spring Boot application and MySQL database. It includes configurations for persistent storage, deployments, and services, as well as instructions for creating secrets and applying the manifests.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Directory Structure](#directory-structure)
- [Components](#components)
  - [Namespace](#namespace)
  - [MySQL Storage](#mysql-storage)
  - [MySQL Deployment and Service](#mysql-deployment-and-service)
  - [Spring Boot Deployment and Service](#spring-boot-deployment-and-service)
  - [Creating Secrets](#creating-secrets)
- [Deployment Steps](#deployment-steps)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Prerequisites

- A Kubernetes cluster up and running.
- `kubectl` command-line tool installed and configured to interact with your cluster.
- Docker image for your Spring Boot application is available and accessible (replace `bharathoptdocker/my_spring_application:version1` with your Docker image name and tag).

## Directory Structure

```plaintext
kubernetes/
├── manifests/
│   ├── namespace.yaml
│   ├── mysql-pv.yaml
│   ├── mysql-pvc.yaml
│   ├── mysql-deployment.yaml
│   ├── mysql-service.yaml
│   ├── springboot-deployment.yaml
│   ├── springboot-service.yaml
```

## Components

### Namespace

**`namespace.yaml`**

Defines the `spring-example` namespace for isolating resources.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: spring-example
```

### MySQL Storage

**`mysql-pv.yaml`**

Defines the Persistent Volume for MySQL storage.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mysql-pv-volume
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data/mysql"
```

**`mysql-pvc.yaml`**

Defines the Persistent Volume Claim for MySQL storage.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pv-claim
  namespace: spring-example
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

### MySQL Deployment and Service

**`mysql-deployment.yaml`**

Deploys the MySQL container and sets environment variables.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
  namespace: spring-example
spec:
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
      - image: mysql:5.7
        name: mysql
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "Prajna@2003"
        ports:
        - containerPort: 3306
          name: mysql
        volumeMounts:
        - name: mysql-persistent-storage
          mountPath: /var/lib/mysql
        command:
        - /bin/bash
        - -c
        - |
          tail -f /dev/null
      volumes:
      - name: mysql-persistent-storage
        persistentVolumeClaim:
          claimName: mysql-pv-claim
```

**`mysql-service.yaml`**

Exposes MySQL on NodePort for external access.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql
  namespace: spring-example
spec:
  type: NodePort
  ports:
    - port: 3306
      targetPort: 3306
      nodePort: 30006  # Choose a port within the range 30000-32767
  selector:
    app: mysql
```

### Spring Boot Deployment and Service

**`springboot-deployment.yaml`**

Deploys the Spring Boot application and configures the database connection.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spring-app
  namespace: spring-example
spec:
  replicas: 1
  selector:
    matchLabels:
      app: spring-app
  template:
    metadata:
      labels:
        app: spring-app
    spec:
      containers:
      - name: spring-app
        image: bharathoptdocker/my_spring_application:version1  # Replace with your Docker image name and tag
        ports:
        - containerPort: 7071  # Ensure this matches the port your Spring Boot application is listening on
        env:
        - name: SPRING_DATASOURCE_URL
          value: "jdbc:mysql://mysql:3306/recipes"
        - name: SPRING_DATASOURCE_USERNAME
          value: "root"
        - name: SPRING_DATASOURCE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: mysql-root-password
```

**`springboot-service.yaml`**

Exposes the Spring Boot application on NodePort for external access.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: spring-app-service
  namespace: spring-example
spec:
  type: NodePort  # Changed to NodePort to expose outside the cluster
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30080  # Optional: specify a port in the range 30000-32767
  selector:
    app: spring-app
```

### Creating Secrets

Create the `mysql-secret` using the following command:

```bash
kubectl create secret generic mysql-secret \
  --from-literal=mysql-root-password=Prajna@2003 \
  --namespace=spring-example
```

### Deployment Steps

1. **Apply the Namespace:**

   ```bash
   kubectl apply -f kubernetes/manifests/namespace.yaml
   ```

2. **Deploy MySQL Persistent Storage:**

   ```bash
   kubectl apply -f kubernetes/manifests/mysql-pv.yaml
   kubectl apply -f kubernetes/manifests/mysql-pvc.yaml
   ```

3. **Deploy MySQL:**

   ```bash
   kubectl apply -f kubernetes/manifests/mysql-deployment.yaml
   kubectl apply -f kubernetes/manifests/mysql-service.yaml
   ```

4. **Deploy Spring Boot Application:**

   ```bash
   kubectl apply -f kubernetes/manifests/springboot-deployment.yaml
   kubectl apply -f kubernetes/manifests/springboot-service.yaml
   ```

5. **Create the MySQL Secret:**

   ```bash
   kubectl create secret generic mysql-secret \
     --from-literal=mysql-root-password=Prajna@2003 \
     --namespace=spring-example
   ```

### Verification

To verify that the deployment is successful, you can check the status of the resources:

- **Check Pods:**

  ```bash
  kubectl get pods -n spring-example
  ```

- **Check Services:**

  ```bash
  kubectl get services -n spring-example
  ```

- **Check Deployments:**

  ```bash
  kubectl get deployments -n spring-example
  ```

- **Check Logs for Spring Boot Application:**

  ```bash
  kubectl logs -f deployment/spring-app -n spring-example
  ```

- **Check Logs for MySQL:**

  ```bash
  kubectl logs -f deployment/mysql -n spring-example
  ```

### Troubleshooting

- **If the Spring Boot application cannot connect to MySQL:**

  Ensure that `SPRING_DATASOURCE_URL` is correctly set and that the MySQL service is reachable.

- **If there are issues with persistent storage:**

  Check the Persistent Volume and Persistent Volume Claim statuses:

  ```bash
  kubectl get pv
  kubectl get pvc -n spring-example
  ```

- **If pods are not running:**

  Check the events and describe the pods for more details:

  ```bash
  kubectl describe pod <pod-name> -n spring-example
  kubectl get events -n spring-example
  ```
Adjust the details as needed based on your specific setup and requirements.
