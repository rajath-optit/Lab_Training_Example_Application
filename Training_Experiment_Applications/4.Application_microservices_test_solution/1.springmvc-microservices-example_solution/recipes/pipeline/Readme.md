## Jenkins Pipelines for Spring Boot Application and MySQL Deployment

This repository contains two Jenkins pipelines:

1. **`pipeline.jenkins`**: This pipeline handles the building and publishing of Docker images for the Spring Boot application, and deploys the MySQL service to a Kubernetes cluster.
2. **`deployment.jenkins`**: This pipeline deploys the Spring Boot application to the Kubernetes cluster and sets up necessary Kubernetes resources.

### `pipeline.jenkins`

The `pipeline.jenkins` pipeline is responsible for building the Docker image for the Spring Boot application, publishing it to Docker Hub, and deploying the MySQL service in the Kubernetes cluster.

#### Pipeline Structure

```groovy
pipeline {
    agent any

    environment {
        MAVEN_HOME = '/opt/apache-maven-3.6.3'
        PATH = "${MAVEN_HOME}/bin:${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    git branch: 'main',
                        credentialsId: 'bharath',
                        url: 'https://github.com/optit-cloud-team/optit-lab-springmvc-example.git'
                }
            }
        }

        stage('Deploy the MySQL service in Kubernetes') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'poc-kube-cluster-cred-1', variable: 'KUBECONFIG')]) {
                        sh "kubectl apply -f recipes/kubernetes/manifests/mysql-secret.yaml"
                        sh "kubectl apply -f recipes/kubernetes/manifests/mysql-storage/mysql-pv.yaml"
                        sh "kubectl apply -f recipes/kubernetes/manifests/mysql-storage/mysql-pvc.yaml"
                        sh "kubectl apply -f recipes/kubernetes/manifests/mysql-deployment.yaml -n spring-example"
                        sh "kubectl apply -f recipes/kubernetes/manifests/mysql-service.yaml -n spring-example"
                    }
                }
            }
        }

        stage('Maven Build') {
            steps {
                script {
                    sh "pwd && cd recipes && mvn clean install"
                }
            }
        }

        stage('Verify Dockerfile') {
            steps {
                script {
                    sh 'pwd && ls -la recipes'
                }
            }
        }
        
        stage('Build Docker Images') {
            steps {
                script {
                    dir('recipes') {
                        sh "docker build -f Dockerfile -t bharathoptdocker/my_spring_application:latest ."
                        sh 'docker images'
                    }
                }
            }
        }

        stage('Docker Publish') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'bkdockerid', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin'
                        sh 'docker push bharathoptdocker/my_spring_application:latest'
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
```

#### Explanation of Stages

- **`Checkout`**: Checks out the `main` branch from the Git repository using the specified credentials.

- **`Deploy the MySQL service in Kubernetes`**: Applies Kubernetes manifests for MySQL including secrets, storage, PVCs, deployment, and service.

- **`Maven Build`**: Runs `mvn clean install` to build the Maven project. This step assumes that the `pom.xml` is located in the `recipes` directory.

- **`Verify Dockerfile`**: Lists files in the `recipes` directory to ensure the `Dockerfile` is present.

- **`Build Docker Images`**: Builds a Docker image for the Spring Boot application and lists all Docker images.

- **`Docker Publish`**: Logs in to Docker Hub and pushes the built Docker image to the Docker Hub repository.

- **`post`**: Prints a success or failure message based on the outcome of the pipeline.

### `deployment.jenkins`

The `deployment.jenkins` pipeline is responsible for deploying the Spring Boot application to the Kubernetes cluster and verifying the deployment.

#### Pipeline Structure

```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                script {
                    git branch: 'main',
                    credentialsId: 'bharath',
                    url: 'https://github.com/optit-cloud-team/optit-lab-springmvc-example.git'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'poc-kube-cluster-cred-1', variable: 'KUBECONFIG')]) {
                        sh "kubectl apply -f recipes/kubernetes/manifests/springboot-deployment.yaml -n spring-example"
                        sh "kubectl apply -f recipes/kubernetes/manifests/springboot-service.yaml -n spring-example"
                        sh "kubectl apply -f recipes/kubernetes/manifests/ingress.yaml -n spring-example"
                    }
                }
            }
        }

        stage('Verify Kubernetes Deployment') {
            steps {
                script {
                    sh "kubectl get all -n spring-example"
                }
            }
        }
    }
}
```

#### Explanation of Stages

- **`Checkout`**: Checks out the `main` branch from the Git repository using the specified credentials.

- **`Deploy to Kubernetes`**: Applies Kubernetes manifests for the Spring Boot application deployment, service, and ingress.

- **`Verify Kubernetes Deployment`**: Retrieves and displays the status of all resources in the `spring-example` namespace.

### Additional Resources

- **[Jenkins Documentation](https://www.jenkins.io/doc/)**
- **[Kubernetes Documentation](https://kubernetes.io/docs/home/)**
- **[Docker Documentation](https://docs.docker.com/)**
- **[Maven Documentation](https://maven.apache.org/guides/index.html)**
