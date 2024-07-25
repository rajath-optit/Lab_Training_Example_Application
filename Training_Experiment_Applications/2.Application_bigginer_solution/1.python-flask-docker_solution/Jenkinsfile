pipeline {
    agent any

    stages {
        stage('Git Checkout') {
            steps {
                script {
                    git branch: 'masters',
                        credentialsId: 'rajath-my-git-pat',
                        url: 'https://github.com/rajath-optit/python-flask-docker-hello-world.git'
                    echo "Checked out Git repository"
                }
            }
        }

        stage('Build with Python') {
            steps {
                script {
                    // Assuming your Python script is in the root directory of your repository
                    sh 'python app.py' // Command to execute Python script
                }
            }
        }
    }
}
