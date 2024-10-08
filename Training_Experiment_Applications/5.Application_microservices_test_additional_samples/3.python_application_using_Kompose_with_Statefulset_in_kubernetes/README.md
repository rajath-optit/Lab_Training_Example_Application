# Microservice communication with RabbitMQ using Kompose + statefull.

![image](https://github.com/rajath-optit/Application_python_using-_Kompose_with_Statefulset/assets/128474801/07f6d1db-18a3-4c32-bc3f-38623d927961)

# NOTE: This is basic kompose usage example with statefulSet, any more adjustment can be made as per your requirement.This should help beginners understand how to get started with your application and the role of StatefulSets in Kubernetes.

# NOTE:
 ```
A StatefulSet is used in Kubernetes for applications that require stable and unique network identifiers, persistent storage, and ordered, graceful deployment and scaling. In your setup, the MySQL database is a suitable candidate for a StatefulSet due to the following reasons:

Reasons for Using StatefulSet for MySQL:
Persistent Storage:

MySQL requires persistent storage to ensure data durability and consistency. When a MySQL pod is restarted, the data must be preserved. StatefulSets, combined with Persistent Volume Claims (PVCs), ensure that each pod gets its own persistent storage that remains consistent across restarts.
Stable Network Identifiers:

StatefulSets provide stable network identities (DNS names) for each of their pods. This is crucial for databases like MySQL where the identity of each node needs to remain stable for the database cluster to function correctly.
Ordered Deployment and Scaling:

StatefulSets ensure that pods are started, stopped, and scaled in an ordered sequence. This ordered deployment and scaling are important for maintaining the consistency and integrity of the MySQL database.
Unique Pod Identity:

Each pod in a StatefulSet has a unique identity that is comprised of a stable, unique hostname. This identity is important for applications like MySQL that might require each instance to be uniquely identifiable.
```

To convert your Docker Compose setup to Kubernetes StatefulSets using `kompose`, follow these steps:

1. **Install Kompose**: Ensure you have `kompose` installed. You can install it via the following command:
    ```sh
    curl -L https://github.com/kubernetes/kompose/releases/download/v1.25.0/kompose-linux-amd64 -o kompose
    chmod +x kompose
    sudo mv ./kompose /usr/local/bin/kompose
    ```

2. **Convert Docker Compose to Kubernetes**:
    Run the `kompose` command to convert your `docker-compose.yml` to Kubernetes manifests.
    ```sh
    kompose convert -f docker-compose.yml
    ```

    This will generate a set of YAML files for Kubernetes resources.

3. **Modify the Generated Kubernetes Manifests**:
    Open the generated YAML files and modify them as needed. Specifically, convert the relevant deployments to StatefulSets.

4. **Apply the Kubernetes Manifests**:
    Apply the generated and modified Kubernetes manifests using `kubectl`.
    ```sh
    kubectl apply -f <generated-file>.yaml
    ```

Here's an example of what you might need to adjust in the generated files:

### 1. Convert Deployments to StatefulSets

For services that require persistent storage, such as MySQL, you should convert the generated Deployment to a StatefulSet. Here's an example:

**mysql_db-deployment.yaml** (generated by kompose):
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql-db
spec:
  selector:
    matchLabels:
      app: mysql-db
  serviceName: mysql
  replicas: 1
  template:
    metadata:
      labels:
        app: mysql-db
    spec:
      containers:
      - name: mysql
        image: mysql:5.7
        env:
        - name: MYSQL_DATABASE
          value: "ims"
        - name: MYSQL_ROOT_PASSWORD
          value: "pesuims"
        ports:
        - containerPort: 3306
        volumeMounts:
        - name: mysql-persistent-storage
          mountPath: /var/lib/mysql
  volumeClaimTemplates:
  - metadata:
      name: mysql-persistent-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
```

### 2. Ensure Persistent Volumes and Claims

Ensure the Persistent Volume Claims are correctly defined in the generated YAML. For example:

**mysql-db-claim0-persistentvolumeclaim.yaml**:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-persistent-storage
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

### 3. Services

Ensure that services are correctly defined to expose the StatefulSets:

**mysql-db-service.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql-db
spec:
  ports:
    - port: 3306
  selector:
    app: mysql-db
  clusterIP: None
```

### 4. Deployment for Stateless Applications

The producer and consumers can remain as Deployments, since they do not require persistent storage. Here is an example for the producer:

**producer-deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: producer
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
        image: <your-registry>/producer:latest
        ports:
        - containerPort: 5000
        env:
        - name: RABBITMQ_HOST
          value: rabbitmq
        - name: RABBITMQ_PORT
          value: "5672"
        - name: RABBITMQ_USERNAME
          value: guest
        - name: RABBITMQ_PASSWORD
          value: guest
```

Repeat similar steps for all other microservices (consumers).

5. **Applying the Manifests**:
    Finally, apply all the generated and modified manifests:
    ```sh
    kubectl apply -f .
    ```

This setup ensures that your MySQL database runs as a StatefulSet with persistent storage, while other services run as Deployments. Adjustments might be necessary depending on the specifics of your setup and requirements.

----------------------------------------------------------------------------------------over-view-----------------------------------------------------------------------------------------------

# extra steps used:

1. Organize and Modify Manifests
Since Kompose has generated the manifests, you might need to make some adjustments:

Organize Manifests
Move the generated manifests into separate directories for better organization:
```
mkdir -p ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/statefulset
mkdir -p ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/deployment
mkdir -p ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/service
mv ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/mysql-db-deployment.yaml ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/statefulset/
mv ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/mysql-db-service.yaml ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/service/
mv ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/producer-deployment.yaml ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/deployment/
mv ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/producer-service.yaml ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/service/
mv ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/rabbitmq-deployment.yaml ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/deployment/
mv ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/rabbitmq-service.yaml ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/service/
mv ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/consumer-one-deployment.yaml ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/deployment/
mv ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/consumer-two-deployment.yaml ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/deployment/
mv ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/consumer-three-deployment.yaml ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/deployment/
mv ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/consumer-four-deployment.yaml ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/deployment/
mv ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/db-persistentvolumeclaim.yaml ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/statefulset/
mv ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/mysql-db-claim1-persistentvolumeclaim.yaml ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/statefulset/
```
before organishing converted kompose will look like below image
![image](https://github.com/rajath-optit/Application_python_using-_Kompose_with_Statefulset/assets/128474801/c75e80e0-3607-46f0-9bb5-82345c8606eb)

after organishing converted kompose will look like below image
![image](https://github.com/rajath-optit/Application_python_using-_Kompose_with_Statefulset/assets/128474801/7ba4a823-b9d7-400d-8337-58fb7d8f81e4)


step2:
Modify MySQL StatefulSet and PVC
mysql-db-deployment.yaml should be changed to a StatefulSet. You need to manually adjust it since Kompose generates a Deployment for MySQL. Here’s an example StatefulSet configuration:

```
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql-db
spec:
  serviceName: "mysql"
  replicas: 1
  selector:
    matchLabels:
      app: mysql-db
  template:
    metadata:
      labels:
        app: mysql-db
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        ports:
        - containerPort: 3306
        env:
        - name: MYSQL_DATABASE
          value: "ims"
        - name: MYSQL_ROOT_PASSWORD
          value: "pesuims"
        volumeMounts:
        - name: mysql-persistent-storage
          mountPath: /var/lib/mysql
  volumeClaimTemplates:
  - metadata:
      name: mysql-persistent-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
```
Replace mysql-db-deployment.yaml with the above StatefulSet configuration and remove the mysql-db-claim1-persistentvolumeclaim.yaml file if it's redundant.

Update mysql-db-service.yaml to ensure it matches the StatefulSet:

if service is already looking like this below then change it as per statefulSet requirement.
```
apiVersion: v1
kind: Service
metadata:
  annotations:
    kompose.cmd: /snap/kompose/19/kompose-linux-amd64 convert
    kompose.version: 1.21.0 (992df58d8)
  creationTimestamp: null
  labels:
    io.kompose.service: mysql-db
  name: mysql-db
spec:
  ports:
  - name: "3406"
    port: 3406
    targetPort: 3306
  selector:
    io.kompose.service: mysql-db
status:
  loadBalancer: {}
```

it should look like below

```
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  ports:
    - port: 3306
  clusterIP: None
  selector:
    app: mysql-db
```


### in each file manually add images that has been pushed into docker hub
```
Producer:

docker build -t producer-image -f producer/Dockerfile .
Consumer One:

docker build -t consumer-one-image -f consumer_one/Dockerfile .
Consumer Two:

docker build -t consumer-two-image -f consumer_two/Dockerfile .
Consumer Three:

docker build -t consumer-three-image -f consumer_three/Dockerfile .
Consumer Four:

docker build -t consumer-four-image -f consumer_four/Dockerfile .
```
## individual build step and correct command structure.
After building the images, you can run the application using Docker Compose. Update your docker-compose.yml to use these images:

## TAG & Push
# Log in to Docker Hub
docker login
```
# Push the images to Docker Hub
docker tag producer-image bharathoptdocker/python-producer
docker push bharathoptdocker/python-producer

docker tag consumer-one-image bharathoptdocker/python-consumer-one
docker push bharathoptdocker/python-consumer-one

docker tag consumer-two-image bharathoptdocker/python-consumer-two
docker push bharathoptdocker/python-consumer-two

docker tag consumer-three-image bharathoptdocker/python-consumer-three
docker push bharathoptdocker/python-consumer-three

docker tag consumer-four-image bharathoptdocker/python-consumer-four
docker push bharathoptdocker/python-consumer-four
```

# The summary table for troubleshooting Docker image build issues:

### **Docker Build Troubleshooting Summary**

| **Step**                     | **Command/Action**                               | **Description**                                      |
|------------------------------|--------------------------------------------------|------------------------------------------------------|
| **Check Directory Structure** | Ensure `producer`, `consumer_one`, etc., exist  | Verify the paths and contents of the directories.   |
| **Verify Dockerfile Paths**  | Inspect `COPY` commands in Dockerfiles          | Ensure paths are correct and point to the right directories. |
| **Check `.dockerignore`**    | Review `.dockerignore` file                     | Ensure it doesn’t exclude necessary files or directories. |
| **Rebuild Docker Images**    | `docker builder prune` and build images again   | Clear cache and rebuild images with corrected paths. |
| **Example Dockerfiles**      | Review Dockerfile examples                      | Ensure Dockerfiles are correct for each service.     |
| **Validate Build Command**   | `docker build -t my-service ./service`          | Run build commands from the correct directory.       |
| **Verify Docker Build Context** | Ensure you're in the root directory of the project | The build context must include Dockerfile and source directories. |

### **Commands for Each Step**

| **Step**                     | **Commands**                                     |
|------------------------------|--------------------------------------------------|
| **Check Directory Structure** | `ls ./producer`<br>`ls ./consumer_one`<br>...  |
| **Verify Dockerfile Paths**  | Check `COPY` commands in Dockerfiles            |
| **Check `.dockerignore`**    | `cat .dockerignore`                             |
| **Rebuild Docker Images**    | `docker builder prune`<br>`docker build -t my-producer ./producer`<br>`docker build -t my-consumer-one ./consumer_one`<br>... |
| **Example Dockerfiles**      | Inspect `Dockerfile` for `my-producer`, `my-consumer-one`, etc. |
| **Validate Build Command**   | `docker build -t my-producer ./producer`       |
| **Verify Docker Build Context** | `pwd` to verify directory location             |

This table should help you systematically troubleshoot and resolve Docker image build issues.

Example
```
next add the image upon successfull build each seperatly. change image line and policy line in kubernetes file.
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    kompose.cmd: /snap/kompose/19/kompose-linux-amd64 convert
    kompose.version: 1.21.0 (992df58d8)
  creationTimestamp: null
  labels:
    io.kompose.service: consumer-four
  name: consumer-four
  namespace: Kompose_StatefulSet  # [Namespace added here]
spec:
  replicas: 1
  selector:
    matchLabels:
      io.kompose.service: consumer-four
  strategy: {}
  template:
    metadata:
      annotations:
        kompose.cmd: /snap/kompose/19/kompose-linux-amd64 convert
        kompose.version: 1.21.0 (992df58d8)
      creationTimestamp: null
      labels:
        io.kompose.service: consumer-four
    spec:
      containers:
      - env:
        - name: RABBITMQ_HOST
          value: rabbitmq
        - name: RABBITMQ_PASSWORD
          value: guest
        - name: RABBITMQ_PORT
          value: "5672"
        - name: RABBITMQ_USERNAME
          value: guest
        image: bharathoptdocker/python-consumer-four:v1.0.0  # [Updated image tag]
        imagePullPolicy: "Always"   # [Updated image tag to "Always"]
        name: consumer-four
        resources: {}
      restartPolicy: Always
      serviceAccountName: ""
      volumes: null
status: {}
```



2. Apply the Manifests
After organizing and modifying the manifests, apply them to your Kubernetes cluster:

```
# Apply StatefulSet and PVC
kubectl apply -f ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/statefulset/

# Apply Services
kubectl apply -f ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/service/

# Apply Deployments
kubectl apply -f ~/Application_python_using-_Kompose_with_Statefulset/kubernetes/manifest/deployment/
```

3. Verify the Deployment
Check the status of the resources you deployed:
```
kubectl get pods
kubectl get svc
kubectl get statefulsets
kubectl get pvc
```
------------------------------------------ends------------------------------------------------------
access application
ClusterIP Service
If the service is of type ClusterIP, it is only accessible from within the cluster. You can use kubectl port-forward to access it:

Find the service name and port:

kubectl get services --namespace=kompose-statefulset
Forward a local port to the service port:

kubectl port-forward svc/<service-name> <local-port>:<service-port> --namespace=kompose-statefulset
Example:

kubectl port-forward svc/producer 8080:5000 --namespace=kompose-statefulset
Access the service at http://localhost:8080.

# Additional

Find and replace command ubuntu:
file and replace all name using below command.
SED command in UNIX stands for stream editor and it can perform lots of functions on file like searching, find and replace, insertion or deletion. Though most common use of SED command in UNIX is for substitution or for find and replace
 ```
find ./kubernetes/manifest -type f -exec sed -i 's/old_text/new_text/g' {} +
```
find ./kubernetes/manifest -type f -exec sed -i 's/Kompose_StatefulSet/kompose-statefulset/g' {} +
This command finds all files within the ./kubernetes/manifest directory and its subdirectories, and then uses sed to replace the text Kompose_StatefulSet with kompose-statefulset in each file.
 
check changes
```
grep -r "kompose-statefulset" ./kubernetes/manifest
 ```


find and add any line using below command at once.
 ```
find ./kubernetes/manifest -type f -exec sed -i '/metadata:/a \  namespace: kompose-statefulset' {} +
 Explanation
```

find ./kubernetes/manifest -type f: Find all files in the ./kubernetes/manifest directory and its subdirectories.
```
-exec sed -i '/metadata:/a \ namespace: kompose-statefulset' {} +: For each file, use sed to append the line namespace: kompose-statefulset after every occurrence of the line metadata:.
```

# output:

check pod/namespace status using kubectl commands or k9s

![image](https://github.com/rajath-optit/Application_python_using-_Kompose_with_Statefulset/assets/128474801/724fbc47-de56-4ef1-936a-7191107ee791)

![image](https://github.com/rajath-optit/Application_python_using-_Kompose_with_Statefulset/assets/128474801/db7f77f5-bc74-4e46-9eaa-c9ee4581fc6a)

running

### To test whether a StatefulSet is working correctly in Kubernetes, you can follow these steps. These methods help you verify if the StatefulSet's features are functioning as expected.

### **Testing StatefulSet Functionality**

| **Test**                | **Command/Action**                                         | **Description**                                                                                           |
|------------------------|------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| **Check StatefulSet Pods** | `kubectl get pods -l app=your-statefulset-label`         | Verify that the StatefulSet pods are running and have the `Running` status.                            |
| **Verify Pod Names**    | `kubectl get pods -l app=your-statefulset-label`         | Check that the pod names follow the StatefulSet naming convention (e.g., `my-service-0`, `my-service-1`). |
| **Check Pod Logs**      | `kubectl logs my-service-0`                              | Review the logs to see if the application inside the pods is functioning as expected.                   |
| **Inspect Pod Status**  | `kubectl describe pod my-service-0`                       | Inspect details of the pod, including events and conditions.                                            |
| **Test Network Connectivity** | `kubectl exec -it my-service-0 -- ping my-service-1`   | Check if the StatefulSet pods can communicate with each other.                                           |
| **Verify Persistent Storage** | `kubectl exec -it my-service-0 -- df -h`               | Ensure the volume mounts are present and that the storage is accessible.                                 |
| **Check Service Endpoints** | `kubectl get endpoints my-service`                       | Ensure the endpoints for the service are correct and match the StatefulSet pods.                         |
| **Perform Scale Test**  | `kubectl scale statefulset my-service --replicas=3`       | Test scaling by changing the number of replicas and verify if the new pods are created and function.    |
| **Test StatefulSet Rolling Update** | `kubectl rollout restart statefulset my-service` | Verify that the StatefulSet performs rolling updates correctly.                                          |
| **Check Headless Service** | `kubectl get svc my-service`                            | Ensure the headless service is created for the StatefulSet, and check the `clusterIP` is set to `None`.  |
| **Verify Pod Ordering** | `kubectl get pods -o wide`                               | Check the order in which the pods are created and deleted (they should follow the StatefulSet sequence).|
| **Perform Data Persistence Test** | `kubectl exec -it my-service-0 -- sh`                | Create some data in the pod and restart the StatefulSet to verify if the data persists.                 |

### **Detailed Commands and Actions**

| **Test**                      | **Command**                                                | **Expected Outcome**                                            |
|------------------------------|-----------------------------------------------------------|---------------------------------------------------------------|
| **Check StatefulSet Pods**   | `kubectl get pods -l app=your-statefulset-label`         | Pods should be in the `Running` state.                        |
| **Verify Pod Names**        | `kubectl get pods -l app=your-statefulset-label`         | Pods should have sequential names like `my-service-0`, `my-service-1`. |
| **Check Pod Logs**          | `kubectl logs my-service-0`                              | Logs should indicate the application is running correctly.    |
| **Inspect Pod Status**      | `kubectl describe pod my-service-0`                       | Should show `Running` status and check for any warning/errors. |
| **Test Network Connectivity** | `kubectl exec -it my-service-0 -- ping my-service-1`   | Should receive ping responses from other pods.               |
| **Verify Persistent Storage** | `kubectl exec -it my-service-0 -- df -h`                 | Should show mounted persistent volumes.                      |
| **Check Service Endpoints**  | `kubectl get endpoints my-service`                        | Should list the StatefulSet pods as endpoints.                |
| **Perform Scale Test**      | `kubectl scale statefulset my-service --replicas=3`       | New pods should be created, and the scale operation should be successful. |
| **Test StatefulSet Rolling Update** | `kubectl rollout restart statefulset my-service` | New pods should be created and old pods should be deleted in order. |
| **Check Headless Service**  | `kubectl get svc my-service`                              | Service should have `clusterIP: None` and be of type `ClusterIP`. |
| **Verify Pod Ordering**     | `kubectl get pods -o wide`                                | Pods should be created and deleted in a sequential order.      |
| **Perform Data Persistence Test** | `kubectl exec -it my-service-0 -- sh`                 | Data should persist through pod restarts or StatefulSet updates. |

### **Example Commands**
```
# Check if StatefulSet pods are running
kubectl get pods -l app=my-service

# Verify pod names and their order
kubectl get pods -l app=my-service

# Check logs of the first pod
kubectl logs my-service-0

# Inspect the status of the first pod
kubectl describe pod my-service-0

# Test network connectivity between pods
kubectl exec -it my-service-0 -- ping my-service-1

# Verify persistent storage in the first pod
kubectl exec -it my-service-0 -- df -h

# Check the endpoints of the service
kubectl get endpoints my-service

# Scale the StatefulSet
kubectl scale statefulset my-service --replicas=3

# Restart the StatefulSet for a rolling update
kubectl rollout restart statefulset my-service

# Check the headless service
kubectl get svc my-service

# Check the pod ordering and details
kubectl get pods -o wide

# Perform a data persistence test
kubectl exec -it my-service-0 -- sh
```

These tests cover various aspects of a StatefulSet's functionality, including pod management, networking, storage, and updates.


------------------------------------------end---------------------------------------------------

check spring application next :)
