pipeline {
    agent any

    environment {
        DOCKER_PROJECT_NAME = "odh-chatbot"
        DOCKER_IMAGE = '755952719952.dkr.ecr.eu-west-1.amazonaws.com/odh-chatbot'
        DOCKER_TAG = "test-$BUILD_NUMBER"

		SERVER_PORT = "1014"

        CHATBOT_FACEBOOK_CREDENTIALS_TEST = credentials('chatbot-facebook-credentials-test')
        CHATBOT_API_CREDENTIALS_TEST = credentials('chatbot-api-credentials-test')
    }

    stages {
        stage('Configure') {
            steps {
                sh """
                    rm -f .env
                    echo '' > .env
                    echo 'COMPOSE_PROJECT_NAME=${DOCKER_PROJECT_NAME}' >> .env
                    echo 'DOCKER_IMAGE=${DOCKER_IMAGE}' >> .env
                    echo 'DOCKER_TAG=${DOCKER_TAG}' >> .env

					echo 'SERVER_PORT=${SERVER_PORT}' >> .env

                    cat '${CHATBOT_FACEBOOK_CREDENTIALS_TEST}' > fb_credentials.yml
                    cat '${CHATBOT_API_CREDENTIALS_TEST}' > api_credentials.txt
                """
            }
        }
        stage('Build') {
            steps {
                sh '''
                    aws ecr get-login --region eu-west-1 --no-include-email | bash
                    docker-compose --no-ansi -f infrastructure/docker-compose.build.yml build --pull
                    docker-compose --no-ansi -f infrastructure/docker-compose.build.yml push
                '''
            }
        }
        stage('Deploy') {
            steps {
               sshagent(['jenkins-ssh-key']) {
                    sh """
                        (cd infrastructure/ansible && ansible-galaxy install -f -r requirements.yml)
                        (cd infrastructure/ansible && ansible-playbook --limit=test deploy.yml --extra-vars "release_name=${BUILD_NUMBER}")
                    """
                }
            }
        }
    }
}
