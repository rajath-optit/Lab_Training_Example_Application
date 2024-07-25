pipelineJob('MyPipelineJob') {
    definition {
        cps {
            script(readFileFromWorkspace('Jenkinsfile'))
        }
    }
}
