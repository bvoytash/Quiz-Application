// Multibranch Pipeline with Webhook Trigger

pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                // Assuming you have Python 3.10 installed
                script {

                    sh 'python3 -m pip install --upgrade pip'
                    sh 'pip3 install -r requirements.txt'


                }
            }
        }

        stage('Test') {
            steps {
                script {

                    sh 'python3 manage.py test'

                }
            }
        }

        stage('Deploy to Render') {
            steps {
                script {
                    withCredentials([
                        string(credentialsId: 'RENDER_API_KEY', variable: 'RENDER_API_KEY'), 
                        string(credentialsId: 'RENDER_DEPLOY_HOOK', variable: 'RENDER_DEPLOY_HOOK')
                    ]) {
                        // Trigger the redeploy via the Render API

                        sh """
                            curl -X POST https://api.render.com/v1/services/${env.RENDER_DEPLOY_HOOK}/deploys \
                            -H "Authorization: Bearer ${env.RENDER_API_KEY}" \
                            -H "Content-Type: application/json" \
                            -d "{}"
                        """

                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs() // Clean workspace after the build
        }
    }
}