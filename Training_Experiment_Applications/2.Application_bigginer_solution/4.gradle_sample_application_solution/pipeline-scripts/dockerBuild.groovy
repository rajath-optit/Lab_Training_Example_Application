def dockerBuild(String imageName) {
    sh "docker build -t ${imageName} ."
}

return this
