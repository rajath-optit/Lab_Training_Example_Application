# Recipe Management System with Nodeport

The *Recipe Management System* is an MVC web application designed for managing food recipes. It allows users to create, view, edit, and delete recipes, complete with ingredient lists, cooking instructions, and difficulty levels. This guide provides detailed instructions for setting up and deploying the application, integrating it with a MySQL database, and automating the deployment process.


## Manual Deployment and Build Process

This document outlines the steps to manually perform the tasks defined in the Jenkins pipeline for deploying the MySQL service, building the Maven project, and managing Docker images.

### Prerequisites

Ensure that you have the following installed and configured:
- **Git**: For cloning the repository.
- **Docker**: For building and pushing Docker images.
- **Maven**: For building the Maven project.
- **kubectl**: For interacting with the Kubernetes cluster.
- **Kubeconfig**: Ensure you have the Kubeconfig file to access the Kubernetes cluster.
- **Docker Hub Credentials**: Username and password for Docker Hub.

### Steps

#### 1. Checkout the Repository

Clone the repository from GitHub:

```bash
git clone -b main https://github.com/optit-cloud-team/optit-lab-springmvc-example.git
cd optit-lab-springmvc-example
```

#### 2. Deploy the MySQL Service in Kubernetes

Perform the following commands to apply the Kubernetes manifests:

```bash
# Set the KUBECONFIG environment variable
export KUBECONFIG=/path/to/your/kubeconfig/file

# Deploy MySQL Secret
kubectl apply -f recipes/kubernetes/manifests/mysql-secret.yaml

# Deploy MySQL Persistent Volume (PV)
kubectl apply -f recipes/kubernetes/manifests/mysql-storage/mysql-pv.yaml

# Deploy MySQL Persistent Volume Claim (PVC)
kubectl apply -f recipes/kubernetes/manifests/mysql-storage/mysql-pvc.yaml

# Deploy MySQL Deployment
kubectl apply -f recipes/kubernetes/manifests/mysql-deployment.yaml -n spring-example

# Deploy MySQL Service
kubectl apply -f recipes/kubernetes/manifests/mysql-service.yaml -n spring-example
```

#### 3. Build the Maven Project

Navigate to the `recipes` directory and run the Maven build commands:

```bash
cd recipes
mvn clean install
```

#### 4. Verify Dockerfile

Check the presence of the `Dockerfile` in the `recipes` directory:

```bash
pwd
ls -la recipes
```

#### 5. Build Docker Images

Build the Docker image using the Dockerfile:

```bash
cd recipes
docker build -f Dockerfile -t bharathoptdocker/my_spring_application:latest .
```

List Docker images to verify:

```bash
docker images
```

#### 6. Publish Docker Image to Docker Hub

Login to Docker Hub and push the Docker image:

```bash
# Login to Docker Hub
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

# Push Docker image
docker push bharathoptdocker/my_spring_application:latest
```

**Replace** `$DOCKER_USERNAME` and `$DOCKER_PASSWORD` with your Docker Hub credentials.

### Additional Resources

- [Docker CLI Documentation](https://docs.docker.com/engine/reference/commandline/cli/)
- [Maven CLI Documentation](https://maven.apache.org/ref/3.6.3/maven-embedder/cli.html)
- [Kubernetes kubectl Documentation](https://kubernetes.io/docs/reference/kubectl/overview/)

### Troubleshooting

- **MySQL Deployment Issues:** Check Kubernetes logs and describe resources for errors:
  ```bash
  kubectl logs <mysql-pod-name> -n spring-example
  kubectl describe pod <mysql-pod-name> -n spring-example
  ```
- **Docker Build Issues:** Ensure Dockerfile syntax is correct and dependencies are available.
- **Docker Publish Issues:** Verify Docker Hub credentials and network connectivity.


## Deployment Files

Below are the Kubernetes manifests used for deploying MySQL and the Spring Boot application.

### 1. **PersistentVolume and PersistentVolumeClaim**

The `PersistentVolume` (PV) and `PersistentVolumeClaim` (PVC) provide persistent storage for the MySQL database.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mysql-pv
  namespace: spring-example
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /mnt/data
```

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
  namespace: spring-example
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

### 2. **MySQL Deployment and Service**

The `Deployment` for MySQL sets up the database, while the `Service` exposes it via NodePort.

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
      volumes:
      - name: mysql-persistent-storage
        persistentVolumeClaim:
          claimName: mysql-pvc
```

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

### 3. **Spring Boot Application Deployment and Service**

The `Deployment` for the Spring Boot application specifies the container image and environment variables. The `Service` exposes the application via NodePort.

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
          value: "jdbc:mysql://10.10.30.87:30006/recipes"
        - name: SPRING_DATASOURCE_USERNAME
          value: "root"
        - name: SPRING_DATASOURCE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: mysql-root-password
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: spring-app-service
  namespace: spring-example
spec:
  type: NodePort
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30080  # Optional: specify a port in the range 30000-32767
  selector:
    app: spring-app
```

## Configuration Details

### MySQL Configuration

- **Database**: `recipes`
- **Root Password**: `Prajna@2003`
- **Host**: `10.10.30.87` (Node IP Address)
- **Port**: `30006` (NodePort for MySQL)

### Spring Boot Configuration

Add the following configuration to your `application.properties` or `application.yml` file:

```properties
# ===============================
# = DATA SOURCE
# ===============================
spring.datasource.url=jdbc:mysql://10.10.30.87:30006/recipes
spring.datasource.username=root
spring.datasource.password=Prajna@2003
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.tomcat.max-wait=10000
spring.datasource.tomcat.max-active=5
spring.datasource.tomcat.test-on-borrow=true

# ===============================
# = JPA / HIBERNATE
# ===============================
spring.jpa.show-sql = true
spring.jpa.hibernate.ddl-auto = update
spring.jpa.properties.hibernate.dialect = org.hibernate.dialect.MySQLDialect

# ===============================
# = Thymeleaf configurations
# ===============================
spring.thymeleaf.mode=LEGACYHTML5
spring.thymeleaf.cache=false
```

### Accessing the Application

- **Spring Boot Application**: `http://<NODE_IP>:30080`
- **MySQL Database**: Accessible from within the cluster using the `mysql` service name or from outside the cluster using `http://<NODE_IP>:30006`.

## Creating Kubernetes Secrets

To securely store your MySQL root password, create a secret using the following YAML:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secret
  namespace: spring-example
type: Opaque
data:
  mysql-root-password: UHJham5hQDIwMDM=  # Base64 encoded password for "Prajna@2003"
```

Generate the base64 encoded password with the following command:

```sh
echo -n 'Prajna@2003' | base64
```

## Conclusion

This setup uses `NodePort` to expose the MySQL database and Spring Boot application to external traffic. Ensure that you update the `SPRING_DATASOURCE_URL` and MySQL `root` password in your `application.properties` as needed.

## Troubleshooting

- **Application does not connect to the database**: Check the `SPRING_DATASOURCE_URL` and ensure the MySQL service is accessible at the specified NodePort.
- **MySQL Service not reachable**: Verify the `mysql` service and `NodePort` configuration.
- **Spring Boot Application logs**: Check logs for connection issues using `kubectl logs <spring-app-pod-name> -n spring-example`.


#### 7. Clean Up Resources

To remove deployed resources from your Kubernetes cluster, execute the following commands:

```bash
# Delete MySQL Service
kubectl delete -f recipes/kubernetes/manifests/mysql-service.yaml -n spring-example

# Delete MySQL Deployment
kubectl delete -f recipes/kubernetes/manifests/mysql-deployment.yaml -n spring-example

# Delete MySQL Persistent Volume Claim (PVC)
kubectl delete -f recipes/kubernetes/manifests/mysql-storage/mysql-pvc.yaml

# Delete MySQL Persistent Volume (PV)
kubectl delete -f recipes/kubernetes/manifests/mysql-storage/mysql-pv.yaml

# Delete MySQL Secret
kubectl delete -f recipes/kubernetes/manifests/mysql-secret.yaml
```

#### 8. Updating Docker Images

If you need to update the Docker image, follow these steps:

1. **Make Changes:** Update your source code or Dockerfile as needed.
2. **Rebuild Docker Image:** 

    ```bash
    cd recipes
    docker build -f Dockerfile -t bharathoptdocker/my_spring_application:latest .
    ```

3. **Push Updated Image:**

    ```bash
    docker push bharathoptdocker/my_spring_application:latest
    ```

4. **Update Kubernetes Deployment:**

    If the image is updated, you might need to update the Kubernetes deployment to use the new image:

    ```bash
    kubectl set image deployment/my-spring-application my-spring-application=bharathoptdocker/my_spring_application:latest -n spring-example
    ```

### Common Issues and Troubleshooting

#### 1. **Kubernetes Command Issues**

- **Problem:** `kubectl` commands fail or return errors.
- **Solution:** Check that the `KUBECONFIG` environment variable is correctly set and points to the valid kubeconfig file.

    ```bash
    echo $KUBECONFIG
    ```

    Ensure you have the necessary permissions and that your kubeconfig file is not corrupted.

#### 2. **Docker Build Failures**

- **Problem:** Docker build fails due to missing files or errors in the Dockerfile.
- **Solution:** Review the Dockerfile for syntax errors and check that all referenced files are present.

    ```bash
    docker build -f Dockerfile -t test-image .
    ```

    For more detailed error messages, use `--no-cache`:

    ```bash
    docker build --no-cache -f Dockerfile -t test-image .
    ```

#### 3. **Docker Push Issues**

- **Problem:** `docker push` fails with authentication errors.
- **Solution:** Ensure that your Docker Hub credentials are correct and that you have access to the repository.

    ```bash
    docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"
    ```

#### 4. **Maven Build Problems**

- **Problem:** Maven build fails.
- **Solution:** Ensure that Maven is correctly installed and that all required dependencies are available.

    ```bash
    mvn clean install
    ```

    Review error logs for specific issues related to missing dependencies or build failures.

### Best Practices

1. **Version Control:** Keep track of changes to your Dockerfile, Maven POM, and Kubernetes manifests. Use Git for version control.

2. **Testing:** Test your Docker images locally before pushing them to Docker Hub:

    ```bash
    docker run -p 8080:8080 bharathoptdocker/my_spring_application:latest
    ```

3. **Security:** Manage your Docker Hub credentials and kubeconfig files securely. Avoid hardcoding sensitive information in scripts.

4. **Documentation:** Document any changes to your setup or processes in this README to keep it up-to-date for future reference.

5. **Backup:** Regularly back up your Kubernetes configurations and Docker images.

### Example Commands Summary

| Task                              | Command(s)                                                                                     |
|-----------------------------------|-----------------------------------------------------------------------------------------------|
| **Clone Repository**              | `git clone -b main https://github.com/optit-cloud-team/optit-lab-springmvc-example.git`     |
| **Navigate to Directory**        | `cd optit-lab-springmvc-example`                                                               |
| **Deploy MySQL Secret**          | `kubectl apply -f recipes/kubernetes/manifests/mysql-secret.yaml`                             |
| **Deploy MySQL PV**              | `kubectl apply -f recipes/kubernetes/manifests/mysql-storage/mysql-pv.yaml`                  |
| **Deploy MySQL PVC**             | `kubectl apply -f recipes/kubernetes/manifests/mysql-storage/mysql-pvc.yaml`                 |
| **Deploy MySQL Deployment**     | `kubectl apply -f recipes/kubernetes/manifests/mysql-deployment.yaml -n spring-example`     |
| **Deploy MySQL Service**        | `kubectl apply -f recipes/kubernetes/manifests/mysql-service.yaml -n spring-example`        |
| **Build Maven Project**         | `cd recipes && mvn clean install`                                                               |
| **Verify Dockerfile Presence**   | `pwd && ls -la recipes`                                                                         |
| **Build Docker Image**           | `docker build -f Dockerfile -t bharathoptdocker/my_spring_application:latest .`             |
| **List Docker Images**           | `docker images`                                                                                 |
| **Login to Docker Hub**          | `echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin`               |
| **Push Docker Image**            | `docker push bharathoptdocker/my_spring_application:latest`                                   |
| **Update Kubernetes Deployment** | `kubectl set image deployment/my-spring-application my-spring-application=bharathoptdocker/my_spring_application:latest -n spring-example` |

### References

- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Docker CLI Command Reference](https://docs.docker.com/engine/reference/commandline/cli/)
- [Maven Command Line Reference](https://maven.apache.org/ref/3.6.3/maven-embedder/cli.html)
- [Kubernetes kubectl Command Reference](https://kubernetes.io/docs/reference/kubectl/overview/)
- [Docker Hub](https://hub.docker.com/)


output
![image](https://github.com/rajath-optit/spring_with_nodeport/assets/128474801/6cf6cc8c-99c4-4c33-962d-64fe2f3fac85)

[you may get error if used https] [check Recipe Management System with-ingress Repo to tackle this issue.]

-After using nodeport the application was accessable from allocated port(30080)
-[Accesable from every node in vm that is connected to kubernetes]

check ingress next :)
