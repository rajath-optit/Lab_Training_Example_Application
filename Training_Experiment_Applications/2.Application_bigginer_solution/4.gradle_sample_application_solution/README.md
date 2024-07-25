# Simple Sample Service for Opt IT Lab

This application is a simple sample service for deploying in Opt IT Lab K8s cluster.

## Build and Deployment Flow
![image](https://github.com/optit-cloud-team/optit-lab-service/assets/15092596/e9f5b03e-f070-4f6e-afab-03a3b51ac4a3)


## Useful Commands

| Gradle Command	         | Description                                   |
|:---------------------------|:----------------------------------------------|
| `./gradlew bootRun`        | Run the application.                          |
| `./gradlew build`          | Build the application.                        |
| `./gradlew test`           | Run tests.                                    |
| `./gradlew bootJar`        | Package the application as a JAR.             |
| `./gradlew bootBuildImage` | Package the application as a container image. |

After building the application, you can also run it from the Java CLI:

```bash
java -jar build/libs/optit-lab-service-0.0.1-SNAPSHOT.jar
```

## Container tasks

Run Opt IT Lab Service as a container

```bash
docker run --rm --name optit-lab-service -p 8080:8080 optit-lab-service:0.0.1-SNAPSHOT
```

### Container Commands

| Docker Command	              | Description       |
|:-------------------------------:|:-----------------:|
| `docker stop optit-lab-service`   | Stop container.   |
| `docker start optit-lab-service`  | Start container.  |
| `docker remove optit-lab-service` | Remove container. |

## Kubernetes tasks

### Create Deployment for application container

```bash
kubectl create deployment optit-lab-service --image=optit-lab-service:0.0.1-SNAPSHOT
```

### Create Service for application Deployment

```bash
kubectl expose deployment optit-lab-service --name=optit-lab-service --port=8080
```

### Port forwarding from localhost to Kubernetes cluster

```bash
kubectl port-forward service/optit-lab-service 8000:8080
```

### Delete Deployment for application container

```bash
kubectl delete deployment optit-lab-service
```

### Delete Service for application container

```bash
kubectl delete service optit-lab-service
```
