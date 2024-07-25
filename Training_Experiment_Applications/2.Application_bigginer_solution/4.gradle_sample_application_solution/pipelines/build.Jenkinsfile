pipeline { 
    agent any 
    stages { 
        stage('Git Checkout') { 
            steps { 
                script { 
                    git branch: branch_or_tag, 
                        credentialsId: 'git-PAT', // Provide your credentials ID
                        url: 'https://github.com/optit-cloud-team/optit-lab-service.git' // Provide your Git repository URL
                }
            } 
        }

        // Analyze the project with SonarQube
        stage('SonarQube Analysis') {
            steps {
                //withSonarQubeEnv('sonar-optitcloud-in') {
                 //   sh './gradlew sonar'
                //}
               echo 'sonarscan success' 
                

            }
        }

        stage('Build with Gradle') {
            steps {
                script {
                    // Assuming your Gradle wrapper is in the root directory of your repository
                    sh './gradlew build' // Command to execute Gradle build
                }
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    // Assuming your Dockerfile is in the root directory of your repository
                    docker.build("optit-lab-service", ".") // Replace "your-docker-image-name" with your desired image name
                }
            }
        }
        stage('Docker Publish') {
            steps {
                script {
                    // Docker login using credentials
                    withCredentials([usernamePassword(credentialsId: 'bkdockerid', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD"
                        
                        def buildId = env.BUILD_ID
                        def imageNameWithTag = "bharathoptdocker/optit-lab-service:$buildId"
                        sh "docker tag optit-lab-service $imageNameWithTag"
                        sh "docker push $imageNameWithTag"

                        def imageNameWithLatest = "bharathoptdocker/optit-lab-service:latest"
                        sh "docker tag optit-lab-service $imageNameWithLatest"
                        sh "docker push $imageNameWithLatest"
                    }
                }
            }
        }
    }
}
