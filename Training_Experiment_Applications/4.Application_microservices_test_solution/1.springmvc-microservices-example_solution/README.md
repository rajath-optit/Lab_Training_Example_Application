# Recipe Management System

The *Recipe Management System* is an MVC web application designed for managing food recipes. It allows users to create, view, edit, and delete recipes, complete with ingredient lists, cooking instructions, and difficulty levels. This guide provides detailed instructions for setting up and deploying the application, integrating it with a MySQL database, and automating the deployment process.

## Table of Contents

1. [Technology](#technology)
2. [Setup](#setup)
3. [Deployment](#deployment)
   - [1st Way to Deploy: Using Kubernetes](#1st-way-to-deploy-using-kubernetes)
   - [2nd Way to Deploy: Local MySQL Installation](#2nd-way-to-deploy-local-mysql-installation)
4. [DevOps Engineering Practices](#devops-engineering-practices)
5. [File Directory Structure](#file-directory-structure)
6. [Resources](#resources)
7. [Summary](#summary)

## Technology

*Recipe Management System* uses the following technologies:

- **Java** [version: 8]: The language used to write the application.
- **Maven** [version: 3.6]: A tool for managing dependencies and building the project.
- **Spring Boot** [version: 2.2.5.RELEASE]: The framework for creating and running the Spring application.
- **Spring Boot Data JPA** [version: 2.2.5.RELEASE]: A library for easier access and manipulation of relational databases.
- **Spring Boot Thymeleaf** [version: 2.3.0 Release]: A Java template engine for both web and standalone environments.

## Flowchart diagram
![image](https://github.com/optit-cloud-team/optit-lab-springmvc-example/assets/128474801/b5698edd-bc89-4131-ad33-4bfa85545eea)

## Setup
To set up the *Recipe Management System*, follow these steps:

### 1. Clone the Repository

Clone the GitHub repository to your local machine:

```bash
git clone https://github.com/your-username/recipes.git
cd recipes
```

### 2. Build the Project

Build the project using Maven:

```bash
mvn clean install
```
# note: (you will get error in build saying mysql is not configure) [read and use below kubernetes file pv,pvc files to configure mysql and after setting it up again use above "mvn clean install" command.. if mysql is  correctly confurgured then the my build will be successfull]

### 3. Run the Application

Start the Spring Boot application:

```bash
mvn spring-boot:run
```
#note[you can run application right after mysql build configureation is successfull using avove command]

### 4. Access the Application

Open your web browser and go to the following URL:

- **Home Page**: [http://localhost:8080/recipes](http://localhost:8080/recipes) *(check port, it might change as per your configuration..the given port is only example)*

[start]
## Deployment 

### 1st Way to Deploy: Using Kubernetes

This guide outlines the steps for deploying the *Recipe Management System* using Kubernetes with a MySQL database.

#### Step 1: Set Up MySQL

1. **Pull the MySQL Docker Image**

   Download the official MySQL Docker image:

   ```bash
   docker pull mysql:5.7
   ```

   You can find more details in the [MySQL Docker Documentation](https://hub.docker.com/_/mysql).

2. **Create Kubernetes Resources for MySQL**

   Create the necessary Kubernetes resources for MySQL by applying the following YAML files. These files define the MySQL deployment, service, persistent volume, and other configurations.

   - **mysql-pv.yaml**: Persistent Volume configuration.
   - **mysql-pvc.yaml**: Persistent Volume Claim configuration.
   - **mysql-secret.yaml**: Secret for storing MySQL credentials.
   - **mysql-deployment.yaml**: Deployment configuration for MySQL.
   - **mysql-service.yaml**: Service configuration to expose MySQL.

   Apply these configurations:

   ```bash
   kubectl apply -f kubernetes/manifest/mysql-pv.yaml
   kubectl apply -f kubernetes/manifest/mysql-pvc.yaml
   kubectl apply -f kubernetes/manifest/mysql-secret.yaml
   kubectl apply -f kubernetes/manifest/mysql-deployment.yaml
   kubectl apply -f kubernetes/manifest/mysql-service.yaml
   ```

3. **Verify MySQL Deployment**

   Check that all MySQL resources are running:

   ```bash
   kubectl get pods
   ```

   Ensure the MySQL pod is in the `Running` state and the MySQL service has an assigned IP address.

#### Step 2: Configure the Spring Boot Application

1. **Update `application.properties`**

   Edit the `application.properties` file in `src/main/resources` to include your MySQL database connection details:

   ```properties
   spring.datasource.url=jdbc:mysql://<mysql-service-ip>:<mysql-service-port>/recipe_management
   spring.datasource.username=<your-username>
   spring.datasource.password=<your-password>
   spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
   spring.jpa.hibernate.ddl-auto=update
   ```

   Replace `<mysql-service-ip>` and `<mysql-service-port>` with the IP address and port of the MySQL service.

2. **Build the Spring Boot Application**

   Clean and build the application:

   ```bash
   mvn clean install
   ```

   Ensure there are no build errors.

#### Step 3: Create a Docker Image for the Application

1. **Create a Dockerfile**

   Create a Dockerfile to define how the application will be containerized:

   ```dockerfile
   FROM openjdk:11-jre-slim
   COPY target/your-application-snapshot.jar /app/your-application.jar
   ENTRYPOINT ["java", "-jar", "/app/your-application.jar"]
   ```

   Ensure that `your-application-snapshot.jar` matches the built JAR file name from Maven.

2. **Build the Docker Image**

   Build the Docker image for the Spring Boot application:

   ```bash
   docker build -t your-dockerhub-username/recipes:latest .
   ```

   Replace `your-dockerhub-username` with your Docker Hub username.

#### Step 4: Update Kubernetes Manifests for Spring Boot Application

1. **Update `springboot-deployment.yaml`**

   Modify the deployment configuration to use the newly built Docker image:

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: springboot-deployment
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: springboot
     template:
       metadata:
         labels:
           app: springboot
       spec:
         containers:
         - name: springboot
           image: your-dockerhub-username/recipes:latest
           ports:
           - containerPort: 8080
           env:
           - name: SPRING_DATASOURCE_URL
             value: jdbc:mysql://mysql-service:3306/recipe_management
           - name: SPRING_DATASOURCE_USERNAME
             valueFrom:
               secretKeyRef:
                 name: mysql-secret
                 key: mysql-username
           - name: SPRING_DATASOURCE_PASSWORD
             valueFrom:
               secretKeyRef:
                 name: mysql-secret
                 key: mysql-password
   ```

2. **Apply Kubernetes Configurations**

   Deploy the Spring Boot application and other resources:

   ```bash
   kubectl apply -f kubernetes/manifest/springboot-deployment.yaml
   kubectl apply -f kubernetes/manifest/springboot-service.yaml
   kubectl apply -f kubernetes/manifest/ingress.yaml
   ```

3. **Verify the Deployment**

   Check that the Spring Boot application is running and accessible:

   ```bash
   kubectl get pods
   kubectl get services
   ```

   Verify that the Ingress is correctly set up and accessible via your public domain.

### 2nd Way to Deploy: Local MySQL Installation

If you prefer to run MySQL on your local machine, follow these steps:

#### Step 1: Install MySQL

1. **Download MySQL**

   Download MySQL Community Server from the [official MySQL website](https://dev.mysql.com/downloads/mysql/).

2. **Install MySQL**

   Follow the installation instructions for your operating system. For Unix-based systems, you can use package managers like Homebrew for macOS or `apt` for Ubuntu.

   ```bash
   # For macOS using Homebrew
   brew install mysql

   # For Ubuntu
   sudo apt update
   sudo apt install mysql-server
   ```

3. **Start MySQL Service**

   Start the MySQL service:

   ```bash
   sudo systemctl start mysql
   ```

4. **Secure MySQL Installation**

   Run the MySQL secure installation script:

   ```bash
   sudo mysql_secure_installation
   ```

   Follow the prompts to set a root password, remove anonymous users, and improve security.

#### Step 2: Create a Database and User

1. **Log in to MySQL**

   Log in to MySQL as the root user:

   ```bash
   mysql -u root -p
   ```

2. **Create Database and User**

   Execute the following commands to set up the database and user:

   ```sql
   CREATE DATABASE recipes_db;
   CREATE USER 'recipes_user'@'localhost' IDENTIFIED BY 'password';
   GRANT ALL PRIVILEGES ON recipes_db.* TO 'recipes_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

   Replace `password` with a strong password of your choice.

#### Step 3: Update `application.properties`

Update the `application.properties` file in `src/main/resources` with the local MySQL database connection details:

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/recipes_db
spring.datasource.username=recipes_user
spring.datasource.password=password
spring.datasource

```properties
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.jpa.hibernate.ddl-auto=update
```

#### Step 4: Run the Application

Build and run the Spring Boot application:

```bash
mvn clean install
mvn spring-boot:run
```

### 3. Access the Application

Open your web browser and go to:

- **Home Page**: [http://localhost:8080/recipes](http://localhost:8080/recipes) *(GET Method)*

## DevOps Engineering Practices

To ensure a robust deployment pipeline and maintain the quality of your application, consider implementing the following DevOps practices:

### Continuous Integration (CI)

1. **Automated Builds**

   Configure a CI server (like Jenkins, GitHub Actions, or GitLab CI) to automatically build your application upon every commit. 

   **Example Jenkins Pipeline Script**:

   ```groovy
   pipeline {
       agent any
       stages {
           stage('Build') {
               steps {
                   script {
                       sh 'mvn clean install'
                   }
               }
           }
           stage('Docker Build') {
               steps {
                   script {
                       sh 'docker build -t your-dockerhub-username/recipes:latest .'
                   }
               }
           }
           stage('Push Docker Image') {
               steps {
                   script {
                       withDockerRegistry([credentialsId: 'dockerhub-credentials', url: 'https://index.docker.io/v1/']) {
                           sh 'docker push your-dockerhub-username/recipes:latest'
                       }
                   }
               }
           }
       }
   }
   ```

### Continuous Deployment (CD)

1. **Automated Deployment**

   Set up a CD pipeline to deploy your Docker image to your Kubernetes cluster:

   **Example Jenkins Pipeline Script**:

   ```groovy
   pipeline {
       agent any
       stages {
           stage('Deploy') {
               steps {
                   script {
                       sh 'kubectl apply -f kubernetes/manifest/springboot-deployment.yaml'
                       sh 'kubectl apply -f kubernetes/manifest/springboot-service.yaml'
                       sh 'kubectl apply -f kubernetes/manifest/ingress.yaml'
                   }
               }
           }
       }
   }
   ```

2. **Monitor and Rollback**

   Implement monitoring tools like Prometheus and Grafana, and establish rollback mechanisms for failed deployments.

## File Directory Structure

Here’s an overview of the directory structure for the *Recipe Management System*:

```
recipes/
│
├──
│
├── src/                      # Source code
│   ├── main/
│   │   ├── java/             # Java source code
│   │   │   └── com/
│   │   │       └── example/
│   │   │           └── recipes/
│   │   │               ├── controller/   # Controllers for HTTP requests
│   │   │               ├── model/         # JPA entities and data models
│   │   │               ├── repository/    # Repository interfaces for data access
│   │   │               ├── service/       # Business logic and service classes
│   │   │               └── RecipeApplication.java  # Main Spring Boot application class
│   │   └── resources/      # Configuration files and static resources
│   │       ├── application.properties  # Spring Boot configuration properties
│   │       └── templates/  # Thymeleaf HTML templates
│   └── test/               # Test cases
│
├── Dockerfile              # Dockerfile for building the Docker image
├── kubernetes/             # Kubernetes manifests and configuration files
│   ├── manifest/
│   │   ├── mysql-deployment.yaml  # MySQL Deployment configuration
│   │   ├── mysql-pvc.yaml         # MySQL Persistent Volume Claim configuration
│   │   ├── mysql-pv.yaml          # MySQL Persistent Volume configuration
│   │   ├── mysql-secret.yaml      # MySQL Secret configuration
│   │   ├── springboot-deployment.yaml  # Spring Boot Deployment configuration
│   │   ├── springboot-service.yaml     # Spring Boot Service configuration
│   │   └── ingress.yaml           # Ingress configuration
│   └── values.yaml            # Helm chart values file (if using Helm)
│
├── .gitignore                # Git ignore file
├── README.md                 # This README file
└── pom.xml                   # Maven Project Object Model configuration
```

## Resources

- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [MySQL Docker Documentation](https://hub.docker.com/_/mysql)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Maven Documentation](https://maven.apache.org/guides/index.html)
- [Docker Documentation](https://docs.docker.com/get-started/)

## Summary

The *Recipe Management System* is a comprehensive solution for managing recipes with a robust backend and intuitive user interface. This guide has walked you through the setup of the application, deployment strategies using Kubernetes and local MySQL, and best practices for DevOps engineering. Following these steps will ensure that your application is properly configured, deployed, and maintained.

# Additional improvement/changes update will be added below.

message: Nothing ther yet to update.

----------------------------------------------------end-------------------------------------

Access RabbitMQ management interface (if applicable):
Open http://localhost:15672 in your browser and log in with the
 
use default credentials (user name:guest/passwordguest).
![image](https://github.com/optit-cloud-team/optit-lab-springmvc-example/assets/128474801/05cee7c0-4a39-4a4b-b53d-2b27d817292c)

mysql
Check MySQL Connection
To test connectivity to the MySQL service from within the cluster, you can execute a command in a running pod:
```
kubectl exec -it <spring-app-pod> -n spring-example -- mysql -h10.10.30.87 -P30006 -uroot -p
```
Replace <spring-app-pod> with the name of one of your running Spring Boot application pods.

Check Environment Variables in a Pod
To view environment variables (including database connection settings) in the Spring Boot pod:
```
kubectl exec -it <spring-app-pod> -n spring-example -- printenv
```
Replace <spring-app-pod> with the name of one of your running Spring Boot application pods.
![image](https://github.com/optit-cloud-team/optit-lab-springmvc-example/assets/128474801/4e7e71fb-5cc1-42cf-985d-5d719be0dbbf)

MORE
```
# Get MySQL Deployment details
kubectl get deployment mysql -n spring-example -o yaml

# Get MySQL Service details
kubectl get service mysql -n spring-example -o yaml

# Get logs for MySQL Pod
kubectl logs -l app=mysql -n spring-example

# Describe MySQL Deployment
kubectl describe deployment mysql -n spring-example

# Describe MySQL Service
kubectl describe service mysql -n spring-example

# Get the NodePort for MySQL Service
kubectl get service mysql -n spring-example -o=jsonpath='{.spec.ports[0].nodePort}'

# Test MySQL connection from Spring Boot pod
kubectl exec -it <spring-app-pod> -n spring-example -- mysql -h10.10.30.87 -P30006 -uroot -p

# Check environment variables in the Spring Boot pod
kubectl exec -it <spring-app-pod> -n spring-example -- printenv
```
Application.

![image](https://github.com/optit-cloud-team/optit-lab-springmvc-example/assets/128474801/18daa51f-0bcd-4162-aa56-e413b227e917)


# check nodeport Repo next:)
