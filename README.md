# Call for Code Video Transcriber Starter Kit
In an at-home learning environment, many students will gravitate to video lessons. Video can be an excellent way to learn, but instructors sometimes need to provide notes or assigned readings to students who either need additional or alternative ways of learning, or who do not have access to the original video. 

The app you build in this tutorial will enable instructors to provide additional notes to students who are using video and audio tools as their primary way to learn. Teachers can also easily provide written instructions for students who for whatever reason cannot play a video. 

The code and related files for this tutorial are located in the accompanying <a href="https://github.com/Call-for-Code/cfc-covid-19-video-transcriber" target="\_blank">GitHub repo</a>.

## Learning objectives

In this tutorial, you'll learn how to:

* Create a Python app that can extract text from instructional videos using Watson Speech to Text. 
* Translate text using Watson Language Translator and store the resulting transcript IBM Cloud Object Storage. 
* Create a Vue.js frontend that enables users to upload videos and receive the resulting transcription.

## Prerequisites

To complete this tutorial, you must:

* Register for an [IBM Cloud](https://www.ibm.com/account/reg/us-en/signup?formid=urx-42793&eventid=cfc-2020?cm_mmc=OSocial_Blog-_-Audience+Developer_Developer+Conversation-_-WW_WW-_-cfc-2020-ghub-starterkit-education_ov75914&cm_mmca1=000039JL&cm_mmca2=10008917) account.
* Install [`Python 3.6`](https://www.python.org/downloads/).
* Install the [`Pipenv`](https://pypi.org/project/pipenv/) Python packaging tool.
* Install [`Node.js`](https://nodejs.org).
* Install [`Yarn`](https://classic.yarnpkg.com/en/docs/install/).

## Estimated time

This tutorial should take about 30 minutes to complete.


## 1. Set up the services and object storage

1. Login to [IBM Cloud](https://cloud.ibm.com) and create the following services:

    * [IBM Watson Speech to Text](https://www.ibm.com/cloud/watson-speech-to-text)
    * [IBM Watson Language Translator](https://www.ibm.com/watson/services/language-translator/)
    * [IBM Cloud Object Storage](https://www.ibm.com/cloud/object-storage). Note - to view the resulting transcript in the UI, the bucket you create in Cloud Object Storage requires [public access](https://cloud.ibm.com/docs/services/cloud-object-storage/iam/public-access.html).

2. Create an `.env` file in the root project directory containing the following service credentials as environment variables:

```
IAM_AUTHENTICATOR_STT=<api key for speech to text service>
IAM_AUTHENTICATOR_STT_URL=<url for speech to text service>
IAM_AUTHENTICATOR_TRANSLATE=<api key for translation service>
LANGUAGE_TRANSLATOR_SERVICE=<translator service endpoint. e.g. https://api.eu-gb.language-translator.watson.cloud.ibm.com>
COS_API_KEY_ID=<cloud object storage api key>
COS_RESOURCE_CRN=<cloud object storage resource crn. e.g. crn:v1:bluemix:public:iam::::serviceRole:Writer>
COS_AUTH_ENDPOINT=<cloud object storage auth endpoint. e.g. https://iam.cloud.ibm.com/identity/token>
COS_ENDPOINT=<cloud object storage endpoint. e.g. https://s3.eu-gb.cloud-object-storage.appdomain.cloud>
COS_BUCKET_NAME=<cloud object storage bucket name. e.g. transcripts>
```

## 2. Install and run the app

### Server

1. If you have not done so already, install [Python](https://www.python.org/downloads/) and [Pipenv](https://pypi.org/project/pipenv/).
    
2. From your project root, download the project dependencies: 
    
      ```bash
      pipenv install
      ```

3. You can use a `manage.py` file to simplfy running your Flask applications and avoid having to configure environment variables to run your app. To run your application locally, use:  
    
      ```bash 
      python manage.py start
      ```

The `manage.py` utility offers a variety of different run commands to match your situation:

  * `start`: Starts a server in a production setting using `gunicorn`.
  * `run`: Starts a native Flask development server. This includes backend reloading upon file saves and the Werkzeug stack-trace debugger for diagnosing runtime failures in-browser.
  * `livereload`: Starts a development server using the `livereload` package. This includes backend reloading as well as dynamic frontend browser reloading. The Werkzeug stack-trace debugger will be disabled, so this is only recommended when working on frontend development.
  * `debug`: Starts a native Flask development server, but with the native reloader/tracer disabled. This leaves the debug port exposed to be attached to an IDE (such as PyCharm's `Attach to Local Process`).

There are also a few utility commands:

  * `build`: Compiles `.py` files within the project directory into `.pyc` files.
  * `test`: Runs all unit tests inside of the project's `test` directory.

The server is running at: `http://localhost:3000/` in your browser. 

### Frontend UI

1. If you have not done so already, install [`Node.js`](https://nodejs.org) and [`Yarn`](https://classic.yarnpkg.com/en/docs/install/).

2. In a new terminal, change to the `frontend` directory and install the dependencies:
    ```bash 
    cd frontend
    yarn install
    ```
    
3. Launch the frontend application:  

    **Compiles and hot-reloads for development**

    ```bash
    yarn serve
    ```

    **Compiles and minifies for production**

    ```bash
    yarn build
    ```

    **Lints and fixes files**
    
    ```bash
    yarn lint
    ```

The frontend UI is now running at `http://localhost:8080/` in your browser. 


## 3. Deploy the app

The following instructions apply to deploying the Python Flask server. To deploy the frontend UI, follow the [Node.js build and deploy tutorial](https://developer.ibm.com/node/getting-started-node-js-ibm-cloud/).

### Deploying to IBM Cloud

You can [deploy this application to IBM Cloud](https://cloud.ibm.com/developer/appservice/starter-kits/python-flask-app) or [build it locally](#building-locally) by cloning the repo first. Once your app is live, you can access the `/health` endpoint to build out your cloud native application.

Use the button below to deploy this same application to IBM Cloud. This option creates a deployment pipeline, complete with a hosted GitLab project and DevOps toolchain. You will have the option of deploying to either Cloud Foundry or a Kubernetes cluster. [IBM Cloud DevOps](https://www.ibm.com/cloud/devops) services provide toolchains as a set of tool integrations that support development, deployment, and operations tasks inside IBM Cloud. 

<p align="center">
    <a href="https://cloud.ibm.com/developer/appservice/starter-kits/python-flask-app">
    <img src="https://cloud.ibm.com/devops/setup/deploy/button_x2.png" alt="Deploy to IBM Cloud">
    </a>
</p>


### Building locally

To get started building this application locally, you can either run the application natively or use the [IBM Cloud Developer Tools](https://cloud.ibm.com/docs/cli?topic=cloud-cli-getting-started) for containerization and easy deployment to IBM Cloud.

#### Native application development

Native application development was covered in step 2 above when you installed and ran the app. Your application is running at: `http://localhost:3000/` in your browser.

There are two different options for debugging a Flask project:

1. Run `python manage.py runserver` to start a native Flask development server. This comes with the Werkzeug stack-trace debugger, which will present runtime failure stack-traces in-browser with the ability to inspect objects at any point in the trace. For more information, see [Werkzeug documentation](http://werkzeug.pocoo.org/).
    
2. Run `python manage.py debug` to run a Flask development server with debug exposed, but the native debugger/reloader turned off. This grants access for an IDE to attach itself to the process (that is, in PyCharm, use `Run` -> `Attach to Local Process`).

You can also verify the state of your locally running application using the Selenium UI test script included in the `scripts` directory.

> **Note for Windows users:** `gunicorn` is not supported on Windows. You can start the server with `python manage.py run` on your local machine or build and start the Dockerfile.

#### IBM Cloud Developer Tools

Install [IBM Cloud Developer Tools](https://cloud.ibm.com/docs/cli?topic=cloud-cli-getting-started) on your machine by running the following command:

```
curl -sL https://ibm.biz/idt-installer | bash
```

Create an application on IBM Cloud by running:

```bash
ibmcloud dev create
```

This will create and download a starter application with the necessary files needed for local development and deployment.

Your application will be compiled with Docker containers. To compile and run your app, run:

```bash
ibmcloud dev build
ibmcloud dev run
```

This will launch your application locally. When you are ready to deploy to IBM Cloud on Cloud Foundry or Kubernetes, run one of the following commands:

```bash
ibmcloud dev deploy -t buildpack // to Cloud Foundry
ibmcloud dev deploy -t container // to K8s cluster
```

You can build and debug your app locally with:

```bash
ibmcloud dev build --debug
ibmcloud dev debug
```


## Summary

This tutorial has shown you how to build and deploy an app that uses Watson Speech to Text to transcribe video files. This tutorial also covered deploying a Watson Language Translator and IBM Cloud Object Storage. You can use this simple app as a base to add more complex functionality and create a robust learning app that will help instructors and students improve their online learning experience.
