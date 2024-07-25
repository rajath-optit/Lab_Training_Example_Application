## Jenkins Pipelines for Recipe Management System

This section covers the Jenkins pipelines used for building Docker images and deploying the application to Kubernetes.

### Table of Contents

1. [Overview](#overview)
2. [Build Pipeline (`build.jenkins`)](#build-pipeline-buildjenkins)
3. [Deployment Pipeline (`deployment.jenkins`)](#deployment-pipeline-deploymentjenkins)
4. [Best Practices and Improvements](#best-practices-and-improvements)
5. [How to Configure Jenkins](#how-to-configure-jenkins)

### Overview

The Jenkins pipelines automate the process of building Docker images and deploying the application to Kubernetes. 

- **`build.jenkins`**: Handles the building of Docker images, tagging, publishing to Docker Hub, and initial deployment to Kubernetes.
- **`deployment.jenkins`**: Manages the deployment of the Spring Boot application and verification of the Kubernetes deployment.

---

### Build Pipeline (`build.jenkins`)

The `build.jenkins` pipeline is responsible for checking out the code from GitHub, building Docker images using Docker Compose, tagging these images, pushing them to Docker Hub, and deploying the MySQL service to Kubernetes.

#### `build.jenkins` Pipeline Configuration

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
                sh 'docker-compose pull --build -d'
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

#### Stages Explained

- **Checkout**: Checks out the code from the `main` branch of the GitHub repository using the specified credentials.
- **Deploy with Docker Compose**: Builds and deploys Docker images using Docker Compose, and lists the running Docker containers.
- **Tag Docker Images**: Tags the newly built Docker images with specific versions.
- **Docker Publish**: Logs in to Docker Hub and pushes the tagged images to the Docker Hub repository.
- **Deploy to Kubernetes**: Applies the Kubernetes manifests to deploy the MySQL service in the `my-namespace` namespace.

---

### Deployment Pipeline (`deployment.jenkins`)

The `deployment.jenkins` pipeline is used for deploying the Spring Boot application to Kubernetes and verifying the deployment.

#### `deployment.jenkins` Pipeline Configuration

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
                        sh "kubectl delete -f ${manifestsDir}/producer/producer-service.yaml -n my-namespace"
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
}
```

#### Stages Explained

- **Checkout**: Checks out the code from the `main` branch of the GitHub repository using the specified credentials.
- **Deploy to Kubernetes**: Applies the Kubernetes manifests to deploy the Spring Boot application and the Ingress resource in the `my-namespace` namespace.
- **Verify Kubernetes Deployment**: Checks the status of all resources in the `my-namespace` namespace.

---

### Best Practices and Improvements

Here are some best practices and improvements that can be applied to your Jenkins pipelines:

1. **Optimize Docker Compose Commands**: Ensure you're using the latest base images and optimize Docker Compose commands for efficiency.
   
2. **Versioning Strategy**: Use specific version tags for Docker images based on build numbers or commit hashes for traceability.

3. **Automate Cleanup**: Add steps to clean up old Docker images to save disk space and improve performance.

4. **Parallel Stages**: Utilize parallel stages for tasks like Docker image tagging and publishing to speed up the pipeline execution.

---

### How to Configure Jenkins

To use these pipelines in Jenkins, follow these steps:

1. **Create a New Pipeline Job:**
   - Go to Jenkins dashboard.
   - Click on "New Item" and select "Pipeline".
   - Name your job and click "OK".

2. **Configure Pipeline:**
   - In the "Pipeline" section, select "Pipeline script from SCM".
   - Set the "SCM" to "Git" and provide the Git repository URL.
   - Enter the appropriate branch name (e.g., `main`).
   - Add your credentials for the Git repository and Docker Hub.

3. **Add Pipeline Script:**
   - Paste the content of `build.jenkins` or `deployment.jenkins` into the "Script" field.

4. **Add Credentials:**
   - Add credentials for Docker Hub (`bkdockerid`) and Kubernetes (`poc-kube-cluster-cred-1`).

5. **Save and Build:**
   - Click "Save" and then "Build Now" to run the pipeline.

---

By implementing these improvements and best practices, you can optimize your Jenkins pipelines for efficiency, reliability, and maintainability. 

# note: the current code that is available is to help bigginers and contains additional automation.
