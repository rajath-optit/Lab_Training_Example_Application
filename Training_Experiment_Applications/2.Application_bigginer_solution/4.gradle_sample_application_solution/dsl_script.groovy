// dsl_script.groovy

def gitCheckout(branch, url, credentialsId) {
    checkout([
        $class: 'GitSCM',
        branches: [[name: "*/${branch}"]],
        doGenerateSubmoduleConfigurations: false,
        extensions: [],
        userRemoteConfigs: [[url: url, credentialsId: credentialsId]]
    ])
}

def buildWithGradle() {
    sh './gradlew build'
}

def dockerBuild(imageName) {
    sh "docker build -t ${imageName} ."
}

def dockerPublish(imageName, repo, credentialsId) {
    withCredentials([usernamePassword(credentialsId: credentialsId, passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
        sh "docker login -u $USERNAME -p $PASSWORD"
        sh "docker tag ${imageName} ${repo}/${imageName}"
        sh "docker push ${repo}/${imageName}"
    }
}
