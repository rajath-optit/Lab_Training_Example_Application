def buildWithGradle() {
    withEnv(["GRADLE_OPTS=-Dorg.gradle.daemon=false"]) {
        sh './gradlew clean build'
    }
}

return this
