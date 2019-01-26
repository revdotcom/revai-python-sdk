pipeline {
    agent {
        label 'linux && python'
    }
    stages {
        stage("Version Check") {
            steps {
                checkVersion(discoverVersion())
            }
        }
        stage('Build') {
            steps {
                echo 'Building..'
                sh '''
                    virtualenv ./sdk-deploy
                    . ./sdk-deploy/bin/activate
                    python setup.py sdist
                    python setup.py bdist_wheel
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                sh '''
                    . ./sdk-deploy/bin/activate
                    python2.7 -m setup.py test
                    python3.4 -m setup.py test
                    python3.5 -m setup.py test
                    python3.6 -m setup.py test
                    python3.7 -m setup.py test
                '''
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                sh '''
                    . ./sdk-deploy/bin/activate
                    python -m pip install twine
                    twine upload dist/* -u ${PYPI_USER_ID} -p ${PYPI_PASSWORD}
                '''
                tagRepo(discoverVersion())
            }
        }
    }
    post {
        success {
            notifyComplete('SUCCESS')
        }
        failure {
            notifyComplete('FAILURE')
        }
    }
}

// Get version number from PKG-INFO file
def discoverVersion() {
    def pkgFile = readFile("src/rev_ai.egg-info/PKG-INFO")
    versionLine = pkgFile.split('\n')[2] // get line with version number
    assert versionLine =~ /Version(.*)/
    return versionLine.substring(versionLine.lastIndexOf(':')+2, versionLine.length())
}

// Ensure that the version number has been incremented since last release
def checkVersion(version) {
    def tags = sh (script: "git ls-remote https://${env.GIT_CREDENTIALS}@${getRepoUrl()} --tags origin ${version}", returnStdout: true)
    if (tags.trim() != "") {
        error "${version} is already released, please increase the version number for build to publish"
    }
}

// Tag repo with version number so we know this version has been released
def tagRepo(tag) {
    echo "tagging repo with ${tag}"

    // deletes current tag locally, this will make sure if the tag is deleted from remote it would be set again
    sh "git tag -d ${tag} || (exit 0)"
    // see if it's still on remote - needed to avoid overwriting the tag
    sh "git fetch https://${env.GIT_CREDENTIALS}@${getRepoUrl()} --tags"
    // try to tag
    sh "git tag ${tag}"
    sh "git push https://${env.GIT_CREDENTIALS}@${getRepoUrl()} ${tag}"
}

// Get url of github repo
def getRepoUrl() {
    def httpsPrefix = '^(https://)?'

    def matchesHttpsPrefix = "${GIT_URL}" =~ httpsPrefix

    return matchesHttpsPrefix.replaceFirst('')
}

// sends notifications on failed builds or when the build becomes stable again
def notifyComplete(String buildStatus) {
    String SUCCESS = 'SUCCESS'
    String FAILURE = 'FAILURE'

    return
    if (env.NOSLACK_NOTIFICATIONS == 'true')
    {
        echo "Slack notifications are disabled"
        return
    }
    
    // build status of null means successful
    buildStatus =  buildStatus ?: SUCCESS
    def prevBuildResult = currentBuild.getPreviousBuild()?.getResult()
    echo "notifyComplete with status ${buildStatus}, previous build was ${prevBuildResult}"
        
    if (buildStatus == FAILURE)
        slackSend (
            color: '#FF0000', // red
            channel: '#rev-ai-dev',
            message: "${env.JOB_NAME} ${env.BUILD_NUMBER} for release ${discoverVersion()} failed after ${currentBuild.durationString} (<${env.BUILD_URL}|Open>)")
    else if (buildStatus == SUCCESS && prevBuildResult != SUCCESS)
        slackSend (
            color: '#00FF00', // green
            channel: '#rev-ai-dev', 
            message: "${env.JOB_NAME} ${env.BUILD_NUMBER} for release ${discoverVersion()} back to normal after ${currentBuild.durationString} (<${env.BUILD_URL}|Open>)")
}