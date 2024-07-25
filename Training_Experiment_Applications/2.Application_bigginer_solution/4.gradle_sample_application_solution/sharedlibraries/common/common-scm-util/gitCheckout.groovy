def gitCheckout(String branch, String repoUrl, String credentialsId) {
    checkout([
        $class: 'GitSCM',
        branches: [[name: "*/${branch}"]],
        doGenerateSubmoduleConfigurations: false,
        extensions: [],
        userRemoteConfigs: [[url: repoUrl, credentialsId: credentialsId]]
    ])
}

return this
