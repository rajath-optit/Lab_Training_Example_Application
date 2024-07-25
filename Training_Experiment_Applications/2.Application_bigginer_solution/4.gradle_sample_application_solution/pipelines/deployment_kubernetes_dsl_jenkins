pipeline { 
    agent any 
    stages { 
        stage('Git Checkout') { 
            steps { 
                script { 
                    git branch: branch_or_tag, 
                        credentialsId: 'git-PAT', // Provide your credentials ID
                        url: 'https://github.com/optit-cloud-team/optit-lab-service.git' // Provide your Git repository URL
                }
            } 
        }
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'poc-kube-cluster-cred-1', variable: 'KUBECONFIG')]) {
                        sh 'mkdir -p $HOME/.kube/ && cat $KUBECONFIG > $HOME/.kube/config'
                        sh 'kubectl apply -f kubernetes/manifest/deployment.yaml'
                        sh 'kubectl apply -f kubernetes/manifest/service.yaml'
                    }
                }
            }
        }
    }
}
