pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Initialize Database') {
            steps {
                bat 'python database.py'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pytest'
            }
        }

        stage('Build Validation') {
            steps {
                echo 'Build and tests completed successfully.'
            }
        }
    }
}