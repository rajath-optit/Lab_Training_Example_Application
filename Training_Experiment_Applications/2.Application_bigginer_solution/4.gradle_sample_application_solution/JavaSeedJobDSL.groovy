pipelineJob('generated-java-gradle-job') {
    description('Pipeline for Java project using Gradle')

    parameters {
        stringParam('BRANCH_NAME', 'main', 'Branch to build from')
        stringParam('GIT_URL', 'please enter your git repo', 'Git repository URL')
        stringParam('DOCKER_IMAGE_NAME', 'optit-lab-service', 'Docker image name')
        stringParam('DOCKER_REPO', 'please enter your docker repo', 'Docker repository')
    }

    definition {
        cps {
            script(readFileFromWorkspace('JenkinsFile3'))
            sandbox()
        }
    }
}
