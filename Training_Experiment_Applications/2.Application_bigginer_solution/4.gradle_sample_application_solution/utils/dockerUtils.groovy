def dockerBuild(String imageName) {
    docker.build(imageName, ".") // Using parameter for Docker image name
}

def dockerPublish(String imageName, String dockerRepo, String credentialsId) {
    withCredentials([usernamePassword(credentialsId: credentialsId, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
        def buildId = env.BUILD_ID
        def imageNameWithTag = "\${dockerRepo}/\${imageName}:\${buildId}"
        sh "docker login -u \${DOCKER_USERNAME} -p \${DOCKER_PASSWORD}"
        sh "docker tag \${imageName} \${imageNameWithTag}"
        sh "docker push \${imageNameWithTag}"
    }
}
