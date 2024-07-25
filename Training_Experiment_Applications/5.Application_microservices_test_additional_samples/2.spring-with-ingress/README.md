# Recipe Management System with ingress

## Ingress Setup for Spring Boot Application

In this section, we'll cover how to configure an Ingress resource to make your Spring Boot application accessible via both HTTP and HTTPS using NGINX Ingress Controller.

### Prerequisites

- You have a running Kubernetes cluster.
- You have already deployed your Spring Boot application and MySQL database using NodePort services.
- The NGINX Ingress Controller is installed in your cluster. If it is not installed, you can follow the [official installation guide](https://kubernetes.github.io/ingress-nginx/deploy/).

### Ingress Configuration

We will create an Ingress resource to route HTTP and HTTPS traffic to the `spring-app-service` service. This setup allows you to access your application using the domain `myapp.example.com`.

Here is the `ingress.yaml` configuration:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: spring-app-ingress
  namespace: spring-example
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: spring-app-service
            port:
              number: 8080
  tls:
  - hosts:
    - myapp.example.com
    secretName: my-tls-secret
```

#### Explanation of `ingress.yaml` Fields

- **apiVersion**: `networking.k8s.io/v1` specifies the version of the Ingress API.
- **kind**: `Ingress` indicates the resource type.
- **metadata**:
  - **name**: The name of the Ingress resource.
  - **namespace**: The namespace where the Ingress resource is created.
  - **annotations**: Includes the `nginx.ingress.kubernetes.io/rewrite-target` annotation to rewrite requests to the root path (`/`).
- **spec**:
  - **rules**:
    - **host**: The domain name for accessing your application.
    - **http**:
      - **paths**:
        - **path**: Defines the path prefix for the Ingress rule.
        - **pathType**: Specifies that the path should match the prefix.
        - **backend**:
          - **service**:
            - **name**: The name of the service to route traffic to.
            - **port**:
              - **number**: The port on which the service is listening (8080 for `spring-app-service`).
  - **tls**:
    - **hosts**: The host for which the TLS certificate is applied.
    - **secretName**: The name of the Kubernetes secret containing the TLS certificate and key.

### Setting Up TLS

To enable HTTPS, you need a TLS certificate and key stored in a Kubernetes secret. You can create this secret using the following command:

```sh
kubectl create secret tls my-tls-secret --cert=/path/to/tls.crt --key=/path/to/tls.key -n spring-example
```

Replace `/path/to/tls.crt` and `/path/to/tls.key` with the paths to your TLS certificate and private key files.

### Accessing Your Application

Once the Ingress resource is applied and the TLS secret is set up, you can access your Spring Boot application using the following URLs:

- **HTTP**: `http://myapp.example.com`
- **HTTPS**: `https://myapp.example.com`

Make sure to configure your DNS to point `myapp.example.com` to the external IP address of your Ingress Controller.

### Applying the Ingress Resource

To apply the Ingress configuration, run:

```sh
kubectl apply -f ingress.yaml
```

### Troubleshooting

If you encounter issues:

- Ensure the NGINX Ingress Controller is running.
- Verify that the Ingress resource is correctly configured and the rules match your application's service.
- Check the Ingress Controller logs for any error messages:

  ```sh
  kubectl logs -n ingress-nginx deploy/ingress-nginx-controller
  ```

For further information, refer to the [Ingress documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/).


# more will be added below(test going on)

It is making your Spring Boot application accessible via HTTP and HTTPS. 


Few things to check and consider to ensure your Ingress setup is working as expected:

### Review of `ingress.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: spring-app-ingress
  namespace: spring-example
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: spring-app-service
            port:
              number: 8080
  tls:
  - hosts:
    - myapp.example.com
    secretName: my-tls-secret
```

### What to Check in Your Ingress Configuration

1. **Annotation for Rewrite Target**:
   - Your use of `nginx.ingress.kubernetes.io/rewrite-target: /` will rewrite the URL path to `/`. This is fine if you want all requests to be directed to the root path of your Spring Boot application. If you want to preserve the path, this annotation should be adjusted or removed.
   - If you do not need to rewrite the path, you can remove this annotation.

2. **Path Matching**:
   - The `path: /` with `pathType: Prefix` means that all requests to `myapp.example.com` will be directed to `spring-app-service`. If you have specific paths, you might need additional rules.

3. **TLS Configuration**:
   - Ensure that `my-tls-secret` contains the correct TLS certificate and private key. To check if the secret exists and is correct, use:

     ```sh
     kubectl get secret my-tls-secret -n spring-example -o yaml
     ```

   - Ensure that your DNS for `myapp.example.com` points to the external IP address of your Ingress Controller.

4. **Ingress Controller**:
   - Ensure that the NGINX Ingress Controller is running and correctly configured. You can check the controller's logs for errors:

     ```sh
     kubectl logs -n ingress-nginx deploy/ingress-nginx-controller
     ```

5. **Service Port**:
   - Ensure that `spring-app-service` is correctly exposing port `8080` and that the `spring-app` deployment is listening on this port.

6. **Ingress Resource**:
   - After creating the Ingress resource, check that it was applied successfully:

     ```sh
     kubectl get ingress -n spring-example
     ```

   - Check the details of the Ingress resource for correct rules and TLS settings:

     ```sh
     kubectl describe ingress spring-app-ingress -n spring-example
     ```

### Additional Recommendations

1. **Add More Annotations**:
   - You might want to add additional annotations for better Ingress control, such as `nginx.ingress.kubernetes.io/ssl-redirect: "true"` to enforce HTTPS or `nginx.ingress.kubernetes.io/ssl-passthrough: "true"` if you need to pass through SSL.

2. **Check for Proper Certificates**:
   - Ensure that your TLS secret has a valid certificate for `myapp.example.com`. The certificate should not be expired and should match the domain.

3. **Test HTTP and HTTPS Access**:
   - Verify that you can access your application via `http://myapp.example.com` and `https://myapp.example.com` after deploying the Ingress resource.

### Example Ingress with Additional Annotations

Here’s an enhanced example of the `ingress.yaml` with more annotations:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: spring-app-ingress
  namespace: spring-example
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"  # Redirect HTTP to HTTPS
    nginx.ingress.kubernetes.io/ssl-passthrough: "true"  # Enable SSL passthrough
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"  # Enforce HTTPS
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: spring-app-service
            port:
              number: 8080
  tls:
  - hosts:
    - myapp.example.com
    secretName: my-tls-secret
```

### Summary Checklist

| Check                                 | Action                                                        |
|---------------------------------------|---------------------------------------------------------------|
| **Annotation**                         | Verify that `nginx.ingress.kubernetes.io/rewrite-target` is as desired. |
| **Path Matching**                      | Confirm that `path: /` and `pathType: Prefix` match your requirements. |
| **TLS Secret**                         | Ensure `my-tls-secret` contains a valid certificate and key. |
| **DNS Configuration**                 | Verify DNS points to the Ingress Controller's IP address.   |
| **Ingress Controller**                | Ensure NGINX Ingress Controller is running correctly.        |
| **Service Port**                       | Check that `spring-app-service` exposes the correct port.    |
| **Ingress Resource**                  | Validate Ingress resource creation and settings.            |
| **Annotations**                        | Add annotations for HTTPS redirection and SSL passthrough if needed. |
| **Access Test**                        | Test HTTP and HTTPS access to your application.             |


2nd test
Include the Ingress resource within the deployment setup and ensure that your application is accessible via myapp.example.com, you can integrate the Ingress configuration directly into your springboot-deployment.yaml file. You can also use NGINX Ingress Controller as a load balancer.

update your springboot-deployment.yaml to include the Ingress configuration and the necessary annotations for NGINX:

### Complete `springboot-deployment.yaml` with Ingress Resource

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: spring-example

---

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

---

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

---

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

---

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

---

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

---

apiVersion: v1
kind: Service
metadata:
  name: spring-app-service
  namespace: spring-example
spec:
  type: NodePort  # Expose service to the cluster
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30080  # Optional: specify a port in the range 30000-32767
  selector:
    app: spring-app

---

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: spring-app-ingress
  namespace: spring-example
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"  # Redirect HTTP to HTTPS
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"  # Enforce HTTPS
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: spring-app-service
            port:
              number: 8080
  tls:
  - hosts:
    - myapp.example.com
    secretName: my-tls-secret  # Replace with the name of your TLS secret
```

### Explanation of Key Components

1. **Namespace**:
   - Defines the namespace `spring-example` for your resources.

2. **Persistent Volume and Claim**:
   - Configures persistent storage for MySQL using `hostPath`.

3. **MySQL Deployment and Service**:
   - Deploys the MySQL container and exposes it with a `NodePort` service on port `30006`.

4. **Spring Boot Deployment and Service**:
   - Deploys the Spring Boot application and exposes it with a `NodePort` service on port `30080`.

5. **Ingress Resource**:
   - **Annotations**:
     - `nginx.ingress.kubernetes.io/rewrite-target: /`: Rewrites the incoming request path to `/`.
     - `nginx.ingress.kubernetes.io/ssl-redirect: "true"`: Redirects HTTP traffic to HTTPS.
     - `nginx.ingress.kubernetes.io/force-ssl-redirect: "true"`: Forces the use of HTTPS.

   - **Spec**:
     - **Rules**:
       - **Host**: `myapp.example.com` routes the traffic for this domain.
       - **Path**: `/` with `pathType: Prefix` routes all traffic from the root.
       - **Backend**: Routes traffic to the `spring-app-service` service on port `8080`.

   - **TLS**:
     - **Hosts**: Specifies the host `myapp.example.com` for which the TLS certificate applies.
     - **SecretName**: Refers to the secret containing your TLS certificate and key.

### NGINX Ingress Controller

Ensure that the NGINX Ingress Controller is installed and running. If you haven’t installed it yet, you can do so using the following command:

```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```

This command deploys the NGINX Ingress Controller on your cluster, which handles incoming requests and routes them based on your Ingress rules.

### DNS Configuration

Make sure that the DNS record for `myapp.example.com` points to the external IP address of the NGINX Ingress Controller. You can find this IP address using:

```sh
kubectl get services -o wide -w -n ingress-nginx
```

Look for the `LoadBalancer` service and note its external IP.

### Testing Your Setup

Once everything is configured, test the setup by accessing the following URLs:

- **HTTP**: `http://myapp.example.com` (should redirect to HTTPS)
- **HTTPS**: `https://myapp.example.com`

### Troubleshooting Tips

- **Check Ingress Resource**:

  ```sh
  kubectl get ingress -n spring-example
  ```

- **Describe Ingress Resource**:

  ```sh
  kubectl describe ingress spring-app-ingress -n spring-example
  ```

- **Check NGINX Controller Logs**:

  ```sh
  kubectl logs -n ingress-nginx deploy/ingress-nginx-controller
  ```

- **Verify DNS Resolution**:

  ```sh
  nslookup myapp.example.com
  ```

### Example `README.md` Section for Ingress

Here’s an example section you can include in your README:

---

## Configuring Ingress for the Spring Boot Application

### Overview

This section describes how to configure an Ingress resource to expose your Spring Boot application to the public internet using `myapp.example.com`. We use the NGINX Ingress Controller to handle HTTP and HTTPS traffic and route it to the Spring Boot service.

### Prerequisites

- You have a Kubernetes cluster with the NGINX Ingress Controller installed. If you don’t have it, you can install it using [this guide](https://kubernetes.github.io/ingress-nginx/deploy/).
- Your `spring-app` and `mysql` deployments and services are already set up and running.

### Ingress Configuration

The `ingress.yaml` file configures the rules for routing traffic to your application:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: spring-app-ingress
  namespace: spring-example
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: spring-app-service
            port:
              number: 8080
  tls:
  - hosts:
    - myapp.example.com
    secretName: my-tls-secret
```

### Steps to Deploy

1. **Apply the Ingress Configuration**:

   ```sh
   kubectl apply -f ingress.yaml
   ```

2. **Update DNS Records**:

   Point `myapp.example.com` to the external IP of the

 NGINX Ingress Controller. You can find the IP using:

   ```sh
   kubectl get services -n ingress-nginx
   ```

3. **Verify the Ingress Resource**:

   Check that the Ingress resource is created:

   ```sh
   kubectl get ingress -n spring-example
   ```

4. **Test Access**:

   Visit `https://myapp.example.com` in your browser to see if you can access the Spring Boot application.

### Troubleshooting

- **Check Ingress Logs**:

  ```sh
  kubectl logs -n ingress-nginx deploy/ingress-nginx-controller
  ```

- **Verify TLS Secret**:

  Ensure `my-tls-secret` has the correct certificate and key.

  ```sh
  kubectl get secret my-tls-secret -n spring-example -o yaml
  ```

- **Verify DNS Resolution**:

  ```sh
  nslookup myapp.example.com
  ```

---

Feel free to adjust the content based on your specific needs and environment!

### Summary

To include Ingress in your deployment file and use NGINX as the load balancer, you need to:

1. **Add the Ingress resource to your deployment YAML**.
2. **Include necessary annotations for NGINX**.
3. **Ensure NGINX Ingress Controller is deployed**.
4. **Update DNS to point to the Ingress Controller’s external IP**.
5. **Test HTTP and HTTPS access**.

This approach integrates the Ingress configuration directly into your Kubernetes manifests and sets up a robust environment for your application.
