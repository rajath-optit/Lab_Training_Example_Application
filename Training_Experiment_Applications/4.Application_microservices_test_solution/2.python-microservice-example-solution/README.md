# Microservice communication with RabbitMQ

# Project Documentation
Overview
This project consists of multiple microservices that interact with each other. The services include a producer and several consumers, each with a specific functionality. The project also includes configurations for Docker, Kubernetes, and CI/CD pipelines.

Python Flask Application
This project is built using Python and Flask, a lightweight web framework. Flask is used to create the main application logic and the RESTful APIs for various services. The microservices architecture allows each service to operate independently, making the system more modular and easier to maintain.

### Project directory Structure [after completion]
```
producer/
│
├── producer.py               # Main application logic
├── Dockerfile                # Dockerfile for building the producer component
└── requirements.txt          # Python dependencies for the producer

consumer_one/
│   ├── Dockerfile            # Dockerfile for building consumer_one
│   ├── healthcheck.py        # Consumer_one functionality
│   └── requirements.txt      # Python dependencies for consumer_one

consumer_two/
│   ├── Dockerfile            # Dockerfile for building consumer_two
│   ├── item_creation.py      # Consumer_two functionality
│   ├── requirements.txt      # Python dependencies for consumer_two
│   └── repository/           # Repository module for consumer_two
│       ├── __init__.py
│       ├── database.py
│       └── entity.py

consumer_three/
│   ├── Dockerfile            # Dockerfile for building consumer_three
│   ├── stock_management.py   # Consumer_three functionality
│   └── requirements.txt      # Python dependencies for consumer_three

consumer_four/
│   ├── Dockerfile            # Dockerfile for building consumer_four
│   ├── order_processing.py   # Consumer_four functionality
│   └── requirements.txt      # Python dependencies for consumer_four

dockercompose/
│   ├── docker-compose.yml    # Docker Compose file for deploying the entire application

pipeline_files/
│   ├── build.pipeline        # Jenkins pipeline for building the application
│   ├── deployment.pipeline   # Jenkins pipeline for deploying the application
│   └── shared_library/       # Shared Jenkins library for reusable functions

kubernetes/
│   ├── manifest/
│   │   ├── consumer_one/
│   │   │   ├── consumer-one-deployment.yaml
│   │   │   └── consumer-one-service.yaml
│   │   │
│   │   ├── consumer_two/
│   │   │   ├── consumer-two-deployment.yaml
│   │   │   └── consumer-two-service.yaml
│   │   │
│   │   ├── consumer_three/
│   │   │   ├── consumer-three-deployment.yaml
│   │   │   └── consumer-three-service.yaml
│   │   │
│   │   ├── consumer_four/
│   │   │   ├── consumer-four-deployment.yaml
│   │   │   └── consumer-four-service.yaml
│   │   │
│   │   ├── producer/
│   │   │   ├── producer-deployment.yaml
│   │   │   └── producer-service.yaml
│   │   │
│   │   ├── rabbitmq/
│   │   │   ├── rabbitmq-statefulset.yaml
│   │   │   └── rabbitmq-service.yaml
│   │   │
│   │   └── mysql/
│   │       ├── mysql-statefulset.yaml
│   │       └── mysql-service.yaml
repository/
├── __init__.py
├── database.py
├── entity.py
└── README.md
```


# Inventory Management System [DETAILED OVERVIEW OF APPLICATION]

## Overview

The Inventory Management System is designed to handle inventory operations using a microservice architecture with RabbitMQ as the messaging system. It consists of a producer and multiple consumers, each handling specific tasks.

## Architecture

The system is built using the following components:

- **Producer**: Sends messages to RabbitMQ queues.
- **Consumers**: Process messages from RabbitMQ queues.
- **MySQL Database**: Stores inventory data.
- **RabbitMQ**: Message broker for communication between services.

## Services

### Producer

The producer is a Flask application that exposes RESTful APIs to send messages to RabbitMQ queues.

#### API Endpoints

- **Healthcheck**: `/healthcheck`
  - Method: `GET`
  - Description: Sends a health check message to the `healthcheck` queue.
  - Response:
    ```json
    {
      "message": "Health check message sent"
    }
    ```

- **Create Item**: `/create_item`
  - Method: `POST`
  - Description: Sends an inventory item creation message to the `create_item` queue.
  - Request Body:
    ```json
    {
      "sku": "IB123456789",
      "name": "Tropicana Apple Juice",
      "label": "juice",
      "price": 25.00,
      "quantity": 50
    }
    ```
  - Response:
    ```json
    {
      "message": "Create item message sent"
    }
    ```

- **Stock Management**: `/stock_management`
  - Method: `POST`
  - Description: Sends a stock management message to the `stock_management` queue.
  - Request Body:
    ```json
    {
      "sku": "IB123456789"
    }
    ```
  - Response:
    ```json
    {
      "message": "Stock management (item delete) message sent"
    }
    ```

- **Order Processing**: `/order_processing`
  - Method: `GET`
  - Description: Sends an order processing message to the `order_processing` queue and waits for a response from the consumer.
  - Response:
    ```json
    [
      {
        "sku": "IB123456789",
        "name": "Tropicana Apple Juice",
        "label": "juice",
        "price": 25.00,
        "quantity": 50
      }
    ]
    ```

### Consumers

#### Consumer One: Healthcheck

Processes health check messages from the `healthcheck` queue.

#### Consumer Two: Item Creation

Processes item creation messages from the `create_item` queue and stores the inventory item in the MySQL database.

#### Consumer Three: Stock Management

Processes stock management messages from the `stock_management` queue and deletes the specified inventory item from the MySQL database.

#### Consumer Four: Order Processing

Processes order processing messages from the `order_processing` queue and returns the list of inventory items as a response.

### Database

The MySQL database stores the inventory data. The database schema is defined in `entity.py`.

### Repository

Contains the database connection setup and initialization.

### Docker

The services are containerized using Docker. The `docker-compose.yml` file defines the multi-container setup.

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Build and run the Docker containers**:
   ```bash
   docker-compose up --build
   ```

3. **Access the Producer API**:
   - Healthcheck: `http://localhost:5000/healthcheck`
   - Create Item: `http://localhost:5000/create_item`
   - Stock Management: `http://localhost:5000/stock_management`
   - Order Processing: `http://localhost:5000/order_processing`

## Directory Structure

```plaintext
.
├── consumer_one
│   ├── Dockerfile
│   ├── healthcheck.py
│   └── requirement.txt
├── consumer_two
│   ├── Dockerfile
│   ├── item_creation.py
│   ├── requirement.txt
│   └── repository
│       ├── __init__.py
│       ├── database.py
│       └── entity.py
├── consumer_three
│   ├── Dockerfile
│   ├── stock_management.py
│   ├── requirement.txt
│   └── repository
│       ├── __init__.py
│       ├── database.py
│       └── entity.py
├── consumer_four
│   ├── Dockerfile
│   ├── order_processing.py
│   ├── requirement.txt
│   └── repository
│       ├── __init__.py
│       ├── database.py
│       └── entity.py
├── docker-compose.yml
└── producer
    ├── Dockerfile
    ├── producer.py
    └── requirements.txt
```

## Dependencies

- `pika`: For RabbitMQ messaging
- `flask`: For creating RESTful APIs
- `sqlalchemy`: For ORM with MySQL
- `mysql-connector-python` and `pymysql`: For MySQL connection
- `cryptography`: For secure connections

[DEVOPS PART]

- Ensure that the RabbitMQ and MySQL services are running before starting the producer and consumers.
- The producer service waits for the RabbitMQ and consumer services to be ready before starting.
- The health check consumer logs the received messages, while the item creation, stock management, and order processing consumers interact with the MySQL database.

# DEVOPS STEPS AND FILES
![image](https://github.com/optit-cloud-team/optit-lab-python-microservice-example/assets/128474801/8e28bc2d-0dae-48fb-9916-79efc82274aa)

### DevOps Steps and Pipeline Configuration

#### Kubernetes Manifests

The following manifests are used to deploy the services and applications in Kubernetes:

- **Namespaces:**
  - `my-namespace.yaml`
    ```yaml
    apiVersion: v1
    kind: Namespace
    metadata:
      name: my-namespace
    ```

- **MySQL:**
  - `mysql-storage.yaml/mysql-pvc.yaml`
    ```yaml
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: mysql-pvc
    spec:
      accessModes:
        - ReadWriteOnce
      resources:
        requests:
          storage: 1Gi  # Adjust size as per your requirements
    ```

  - `deployment.yaml`
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

  - `mysql-secret.yaml`

  - `service.yaml`
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

- **Producer:**
  - `producer-deployment.yaml`
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

  - `producer-service.yaml`
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

- **Consumers:**

  Each consumer follows a similar structure. Below is the example for `consumer_one`:

  - `deployment.yaml`
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

  - `service.yaml`
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

  The same structure is repeated for `consumer_two`, `consumer_three`, and `consumer_four` with respective image names and metadata.

#### Jenkins Pipeline Configuration

The Jenkins pipeline automates the deployment process, including Docker image building, tagging, pushing to Docker Hub, and deploying to Kubernetes.

- **Pipeline Definition:**
  
  **Build and Deploy Pipeline:**
  ```groovy
  pipeline {
      agent any

      stages {
          stage('Checkout') {
              steps {
                  script {
                      git branch: 'main',
                      credentialsId: 'bharath',
                      url: 'https://github.com/optit-cloud-team/optit-lab-python-microservice-example.git'
                  }
              }
          }

          stage('Deploy with Docker Compose') {
              steps {
                  // Ensure Docker Compose is installed
                  sh 'docker-compose --version'

                  // Deploy the application using Docker Compose
                  sh 'docker-compose up --build -d'
                  sh 'docker ps'
              }
          }

          stage('Tag Docker Images') {
              steps {
                  sh 'docker tag optit-lab-python-microservice-example-producer:latest bharathoptdocker/python-producer:1'
                  sh 'docker tag optit-lab-python-microservice-example-consumer_one:latest bharathoptdocker/python-consumer-one:1'
                  sh 'docker tag optit-lab-python-microservice-example-consumer_two:latest bharathoptdocker/python-consumer-two:1'
                  sh 'docker tag optit-lab-python-microservice-example-consumer_three:latest bharathoptdocker/python-consumer-three:1'
                  sh 'docker tag optit-lab-python-microservice-example-consumer_four:latest bharathoptdocker/python-consumer-four:1'
              }
          }

          stage('Docker Publish') {
              steps {
                  script {
                      // Docker login using credentials
                      withCredentials([usernamePassword(credentialsId: 'bkdockerid', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                          sh 'echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin'

                          sh 'docker push bharathoptdocker/python-producer:1'
                          sh 'docker push bharathoptdocker/python-consumer-one:1'
                          sh 'docker push bharathoptdocker/python-consumer-two:1'
                          sh 'docker push bharathoptdocker/python-consumer-three:1'
                          sh 'docker push bharathoptdocker/python-consumer-four:1'
                      }
                  }
              }
          }

          stage('Deploy to Kubernetes') {
              steps {
                  script {
                      withCredentials([file(credentialsId: 'poc-kube-cluster-cred-1', variable: 'KUBECONFIG')]) {
                          // Apply Kubernetes manifests in the specified namespace
                          sh 'kubectl apply -f kubernetes/manifest/mysql/service.yaml -n my-namespace'
                          sh 'kubectl apply -f kubernetes/manifest/mysql/mysql-storage.yaml/mysql-pvc.yaml -n my-namespace'
                          sh 'kubectl apply -f kubernetes/manifest/mysql/mysql-secret.yaml -n my-namespace'
                          sh 'kubectl apply -f kubernetes/manifest/mysql/deployment.yaml -n my-namespace'
                      }
                  }
              }
          }
      }
  }
  ```

  **Deployment and Update Pipeline:**
  ```groovy
  pipeline {
      agent any

      stages {
          stage('Checkout') {
              steps {
                  script {
                      git branch: 'main',
                      credentialsId: 'bharath',
                      url: 'https://github.com/optit-cloud-team/optit-lab-python-microservice-example.git'
                  }
              }
          }

          stage('Deploy and Update Deployment') {
              steps {
                  script {
                      def manifestsDir = 'kubernetes/manifest'

                      withCredentials([file(credentialsId: 'poc-kube-cluster-cred-1', variable: 'KUBECONFIG')]) {
                          // Delete deployments
                          sh "kubectl delete -f ${manifestsDir}/producer/producer-deployment.yaml -n my-namespace"
                          sh "kubectl delete -f ${manifestsDir}/consumer_one/deployment.yaml -n my-namespace"
                          sh "kubectl delete -f ${manifestsDir}/consumer_two/deployment.yaml -n my-namespace"
                          sh "kubectl delete -f ${manifestsDir}/consumer_three/deployment.yaml -n my-namespace"
                          sh "kubectl delete -f ${manifestsDir}/consumer_four/deployment.yaml -n my-namespace"

                          // Apply deployments
                          sh "kubectl apply -f ${manifestsDir}/producer/producer-deployment.yaml -n my-namespace"
                          sh "kubectl apply -f ${manifestsDir}/consumer_one/deployment.yaml -n my-namespace"
                          sh "kubectl apply -f ${manifestsDir}/consumer_two/deployment.yaml -n my-namespace"
                          sh "kubectl apply -f ${manifestsDir}/consumer_three/deployment.yaml -n my-namespace"
                          sh "kubectl apply -f ${manifestsDir}/consumer_four/deployment.yaml -n my-namespace"
                      }
                  }
              }
          }

          stage('Deploy and Update Services') {
              steps {
                  script {
                      def manifestsDir = 'kubernetes/manifest'

                      withCredentials([file(credentialsId: 'poc-kube-cluster-cred-1', variable: 'KUBECONFIG')]) {
                          // Delete services
                          sh "kubectl delete -f ${man

ifestsDir}/producer/producer-service.yaml -n my-namespace"
                          sh "kubectl delete -f ${manifestsDir}/consumer_one/service.yaml -n my-namespace"
                          sh "kubectl delete -f ${manifestsDir}/consumer_two/service.yaml -n my-namespace"
                          sh "kubectl delete -f ${manifestsDir}/consumer_three/service.yaml -n my-namespace"
                          sh "kubectl delete -f ${manifestsDir}/consumer_four/service.yaml -n my-namespace"

                          // Apply services
                          sh "kubectl apply -f ${manifestsDir}/producer/producer-service.yaml -n my-namespace"
                          sh "kubectl apply -f ${manifestsDir}/consumer_one/service.yaml -n my-namespace"
                          sh "kubectl apply -f ${manifestsDir}/consumer_two/service.yaml -n my-namespace"
                          sh "kubectl apply -f ${manifestsDir}/consumer_three/service.yaml -n my-namespace"
                          sh "kubectl apply -f ${manifestsDir}/consumer_four/service.yaml -n my-namespace"
                      }
                  }
              }
          }
      }
  } ```

### Additional Notes and Error Handling

- **MySQL Configuration:**
  - Ensure MySQL is configured correctly for the application to function.
  - If deploying in a lab environment, use MySQL version 5.7, which is suitable for lab CPU configurations.
  - Common errors during deployment are often related to MySQL configuration. Check CPU compatibility and deployment methods.

- **Automation:**
  - After configuring Kubernetes, proceed with automation. Jenkins is used here, but GitHub Actions or other CI/CD tools can be used based on your preference.
  - Ensure detailed steps are provided for each stage of the pipeline to avoid confusion during the deployment process.


[addtinal update and recent imporvent].
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                script {
                    git branch: 'main',
                    credentialsId: 'bharath',
                    url: 'https://github.com/optit-cloud-team/optit-lab-python-microservice-example.git'
                }
            }
        }

        stage('Deploy and Update Resources') {
            steps {
                script {
                    def manifestsDir = 'kubernetes/manifest'
                    def deployments = ['producer/producer-deployment.yaml',
                                        'consumer_one/deployment.yaml',
                                        'consumer_two/deployment.yaml',
                                        'consumer_three/deployment.yaml',
                                        'consumer_four/deployment.yaml']
                    def services = ['producer/producer-service.yaml',
                                    'consumer_one/service.yaml',
                                    'consumer_two/service.yaml',
                                    'consumer_three/service.yaml',
                                    'consumer_four/service.yaml']

                    withCredentials([file(credentialsId: 'poc-kube-cluster-cred-1', variable: 'KUBECONFIG')]) {
                        // Delete and Apply Deployments
                        deployments.each { deployment ->
                            sh "kubectl delete -f ${manifestsDir}/${deployment} -n my-namespace || true"
                            sh "kubectl apply -f ${manifestsDir}/${deployment} -n my-namespace"
                        }

                        // Delete and Apply Services
                        services.each { service ->
                            sh "kubectl delete -f ${manifestsDir}/${service} -n my-namespace || true"
                            sh "kubectl apply -f ${manifestsDir}/${service} -n my-namespace"
                        }
                    }
                }
            }
        }
    }
}

# you can also use above pipeline while deployment automation in jenkins. the file contains basic and more understandable code that will help bigginers.

## Jenkins Pipeline Overview

The Jenkins pipeline automates the deployment process for the microservices. It handles the checkout of the code from the repository and the deployment of the application components to the Kubernetes cluster.

## Recent Improvements to the Jenkins Pipeline

### Overview of Improvements

The Jenkins pipeline has been optimized for better efficiency, maintainability, and robustness. Below are the detailed improvements made to the pipeline and the reasons behind them:

### 1. Combined Deployment and Service Stages

**Before:**
Separate stages for deployments and services.

**After:**
Combined into one stage to reduce redundancy and simplify the pipeline.

**Reason:**
Combining similar operations reduces duplication and makes the pipeline easier to maintain. This change simplifies the pipeline structure and improves readability.

**Old Pipeline:**
sh "kubectl delete -f kubernetes/manifest/producer/producer-deployment.yaml -n my-namespace"
sh "kubectl apply -f kubernetes/manifest/producer/producer-deployment.yaml -n my-namespace"
sh "kubectl delete -f kubernetes/manifest/consumer_one/deployment.yaml -n my-namespace"
sh "kubectl apply -f kubernetes/manifest/consumer_one/deployment.yaml -n my-namespace"

New Pipeline:

def deployments = ['producer/producer-deployment.yaml', 'consumer_one/deployment.yaml', 'consumer_two/deployment.yaml', 'consumer_three/deployment.yaml', 'consumer_four/deployment.yaml']
deployments.each { deployment ->
    sh "kubectl delete -f ${manifestsDir}/${deployment} -n my-namespace || true"
    sh "kubectl apply -f ${manifestsDir}/${deployment} -n my-namespace"
}

# Example Enhanced Jenkinsfile with Parameters and Notifications

pipeline {
    agent any

    parameters {
        string(name: 'NAMESPACE', defaultValue: 'my-namespace', description: 'Kubernetes Namespace')
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git Branch')
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Docker Image Tag')
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    git branch: params.BRANCH,
                        credentialsId: 'bharath',
                        url: 'https://github.com/optit-cloud-team/optit-lab-python-microservice-example.git'
                }
            }
        }

        stage('Deploy and Update Resources') {
            steps {
                script {
                    def manifestsDir = 'kubernetes/manifest'
                    def deployments = ['producer/producer-deployment.yaml',
                                        'consumer_one/deployment.yaml',
                                        'consumer_two/deployment.yaml',
                                        'consumer_three/deployment.yaml',
                                        'consumer_four/deployment.yaml']
                    def services = ['producer/producer-service.yaml',
                                    'consumer_one/service.yaml',
                                    'consumer_two/service.yaml',
                                    'consumer_three/service.yaml',
                                    'consumer_four/service.yaml']

                    withCredentials([file(credentialsId: 'poc-kube-cluster-cred-1', variable: 'KUBECONFIG')]) {
                        // Delete and Apply Deployments
                        deployments.each { deployment ->
                            sh "kubectl delete -f ${manifestsDir}/${deployment} -n ${params.NAMESPACE} || true"
                            sh "kubectl apply -f ${manifestsDir}/${deployment} -n ${params.NAMESPACE}"
                        }

                        // Delete and Apply Services
                        services.each { service ->
                            sh "kubectl delete -f ${manifestsDir}/${service} -n ${params.NAMESPACE} || true"
                            sh "kubectl apply -f ${manifestsDir}/${service} -n ${params.NAMESPACE}"
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            mail to: 'team@example.com',
                 subject: 'Pipeline Success',
                 body: 'The pipeline succeeded.'
        }
        failure {
            mail to: 'team@example.com',
                 subject: 'Pipeline Failure',
                 body: 'The pipeline failed.'
        }
    }
}

### Summary of Improvements that you can try.
### Summary of Improvements

| **Improvement**           | **Current**                                                                 | **Improvement**                                                                                   |
|--------------------------|----------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| **Namespace Management** | Creating a custom namespace                                                | Use the default namespace for simplicity.                                                        |
| **Persistent Volume Claim (PVC)** | No `StorageClass` or Secrets                                      | Specify `StorageClass` and use Secrets for sensitive data.                                        |
| **MySQL Configuration** | Hardcoded `MYSQL_ROOT_PASSWORD`                                             | Use Kubernetes Secrets for sensitive data.                                                        |
| **CI/CD Pipeline**      | Combined build, push, deploy steps                                          | Separate stages for build, push, deploy, and add linting/testing.                                |
| **Service Configurations**| Basic service configurations                                              | Add annotations for monitoring/logging.                                                            |
| **Deployment Strategies**| Recreate strategy                                                          | Use `RollingUpdate` for zero-downtime deployments.                                                |
| **Unnecessary Elements**| Hardcoded secrets, static image versions, manual commands                   | Move secrets to Kubernetes Secrets, use versioned tags, automate deployment steps.              |

### How to Use This Table

- **Namespace Management**: Simplify by using the default namespace.
- **Persistent Volume Claim (PVC)**: Add `StorageClass` and manage sensitive data securely.
- **MySQL Configuration**: Handle sensitive data using Kubernetes Secrets.
- **CI/CD Pipeline**: Improve by separating concerns and adding steps for quality checks.
- **Service Configurations**: Enhance configurations with additional features for better management.
- **Deployment Strategies**: Use modern deployment strategies for smoother updates.
- **Unnecessary Elements**: Remove outdated practices for a more robust and automated deployment process.

