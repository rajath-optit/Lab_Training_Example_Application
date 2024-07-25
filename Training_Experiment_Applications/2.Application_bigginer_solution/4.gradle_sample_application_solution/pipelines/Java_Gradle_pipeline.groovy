def call(params) {
    pipeline {
        agent any

        stages {
            stage('Git Checkout') {
                steps {
                    script {
                        gitCheckout(params.BRANCH_NAME, params.GIT_URL, 'git-PAT')
                    }
                }
            }
            stage('Build with Gradle') {
                steps {
                    script {
                        buildWithGradle()
                    }
                }
            }
            stage('Docker Build') {
                steps {
                    script {
                        dockerBuild(params.DOCKER_IMAGE_NAME)
                    }
                }
            }
            stage('Docker Publish') {
                steps {
                    script {
                        dockerPublish(params.DOCKER_IMAGE_NAME, params.DOCKER_REPO, 'bkdockerid')
                    }
                }
            }
        }
    }
}

def gitCheckout(String branch, String gitUrl, String credentialsId) {
    checkout([$class: 'GitSCM',
              branches: [[name: branch]],
              doGenerateSubmoduleConfigurations: false,
              extensions: [],
              submoduleCfg: [],
              userRemoteConfigs: [[url: gitUrl, credentialsId: credentialsId]]
    ])
}

def buildWithGradle() {
    sh './gradlew build'
}

def dockerBuild(String imageName) {
    docker.build(imageName, ".")
}

def dockerPublish(String imageName, String dockerRepo, String credentialsId) {
    withCredentials([usernamePassword(credentialsId: credentialsId, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
        def buildId = env.BUILD_ID
        def imageNameWithTag = "${dockerRepo}/${imageName}:${buildId}"
        sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD"
        sh "docker tag ${imageName} ${imageNameWithTag}"
        sh "docker push ${imageNameWithTag}"
    }
}

return this
