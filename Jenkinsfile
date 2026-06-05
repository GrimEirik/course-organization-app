pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\jetwo\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON%" -m pip install --upgrade pip'
                bat '"%PYTHON%" -m pip install -r requirements.txt'
            }
        }

        stage('Initialize Database') {
            steps {
                bat '"%PYTHON%" database.py'
            }
        }

        stage('Run Tests') {
            steps {
                bat '"%PYTHON%" -m pytest'
            }
        }

        stage('Build Validation') {
            steps {
                echo 'Build and tests completed successfully.'
            }
        }
    }
}