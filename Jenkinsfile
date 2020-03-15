pipeline {
    agent {
        label 'linux && python'
    }
    environment {
        GIT_CREDENTIALS = credentials("${GITHUB_CREDENTIALS}")
    }
    stages {
        stage('Build') {
            agent { docker { image "python:3" } }
            steps {
                echo 'Building..'
                sh '''
                    rm -r dist
                    python3 -m venv ./sdk-deploy
                    . ./sdk-deploy/bin/activate
                    python setup.py sdist bdist_wheel
                '''
            }
        }
        stage('Test') {
            agent {
                dockerfile {
                    label 'linux && python'
                    dir 'tests'
                }
            }
            steps {
                echo 'Testing..'
                sh '''
                    ls ./dist
                    virtualenv ./sdk-test
                    . ./sdk-test/bin/activate
                    tox
                '''
            }
        }
        // stage("Version Check") {
        //     steps {
        //         checkVersion(discoverVersion())
        //     }
        // }
        // stage('Deploy') {
        //     steps {
        //         echo 'Deploying....'
        //         sh '''
        //             . ./sdk-deploy/bin/activate
        //             python -m pip install twine
        //             twine upload dist/* -u ${PYPI_USER_ID} -p ${PYPI_PASSWORD}
        //             rm -r dist
        //         '''
        //         tagRepo(discoverVersion())
        //     }
        // }
    }
    // post {
    //     success {
    //         notifyComplete('SUCCESS')
    //     }
    //     failure {
    //         notifyComplete('FAILURE')
    //     }
    // }
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
    def tags = sh (script: "git ls-remote https://${GIT_CREDENTIALS}@${getRepoUrl()} --tags origin ${version}", returnStdout: true)
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
    sh "git fetch https://${GIT_CREDENTIALS}@${getRepoUrl()} --tags"
    // try to tag
    sh "git tag ${tag}"
    sh "git push https://${GIT_CREDENTIALS}@${getRepoUrl()} ${tag}"
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

    if (env.NOSLACK_NOTIFICATIONS == 'true')
    {
        echo "Slack notifications are disabled"
        return
    }

    // build status of null means successful
    buildStatus =  buildStatus ?: SUCCESS
    def prevBuildResult = currentBuild.getPreviousBuild()?.getResult()
    echo "notifyComplete with status ${buildStatus}, previous build was ${prevBuildResult}"

    // Slack channel ID CFPMB0BK4 refers to #revai-alerts-nonprod, does not change even if channel name changes
    if (buildStatus == FAILURE && prevBuildResult != FAILURE)
        slackSend (
            color: '#FF0000', // red
            channel: 'CFPMB0BK4',
            message: "${env.JOB_NAME} ${env.BUILD_NUMBER} for release ${discoverVersion()} failed after ${currentBuild.durationString} (<${env.BUILD_URL}|Open>)")
    else if (buildStatus == SUCCESS && prevBuildResult != SUCCESS)
        slackSend (
            color: '#00FF00', // green
            channel: 'CFPMB0BK4',
            message: "${env.JOB_NAME} ${env.BUILD_NUMBER} for release ${discoverVersion()} back to normal after ${currentBuild.durationString} (<${env.BUILD_URL}|Open>)")
}
