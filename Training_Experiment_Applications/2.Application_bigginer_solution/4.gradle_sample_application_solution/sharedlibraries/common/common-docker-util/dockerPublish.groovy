def dockerPublish(String imageName, String dockerRepo, String credentialsId) {
    withCredentials([usernamePassword(credentialsId: credentialsId, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
        sh "docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}"
        sh "docker tag ${imageName} ${dockerRepo}/${imageName}"
        sh "docker push ${dockerRepo}/${imageName}"
    }
}

return this
