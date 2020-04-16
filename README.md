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

## Instructions
## 1. Clone the repository
```bash
git clone git@github.com:Call-for-Code/cfc-covid-19-video-transcriber.git
cd cfc-covid-19-video-transcriber
```

## 2. Setup environment variables
Create a `.env` file in the root project directory containing the following environment variables. Note - these will be replaced by your IBM Cloud service credentials in the next step.
```bash
touch .env
```

```
STT_API_KEY=<api key for speech to text service>
STT_URL=<URL for speech to text service>
TRANSLATE_API_KEY=<api key for translator service>
TRANSLATE_URL=<URL for translator service>
COS_API_KEY=<cloud object storage api key>
COS_IAM_ROLE_CRN=<cloud object storage IAM role crn. e.g. crn:v1:bluemix:public:iam::::serviceRole:Writer>
COS_ENDPOINT=<cloud object storage endpoint. e.g. s3.eu-gb.cloud-object-storage.appdomain.cloud>
COS_BUCKET_NAME=<cloud object storage bucket name>
```

## 3. Create IBM Cloud services and obtain service credentials
Register/Login to [IBM Cloud](https://cloud.ibm.com) and create the following services:
   * [IBM Watson Speech to Text](https://www.ibm.com/cloud/watson-speech-to-text)
        * Copy the `apikey` and `url` values within the service credentials to the `STT_API_KEY` and `STT_URL` environment variables in the `.env` file you created in step 2.

   * [IBM Watson Language Translator](https://www.ibm.com/watson/services/language-translator/)
        * Copy the `apikey` and `url` values within the service credentials to the `TRANSLATE_API_KEY` and `TRANSLATE_URL` environment variables in the `.env` file you created in step 2.

   * [IBM Cloud Object Storage](https://www.ibm.com/cloud/object-storage). 
        * Create a standard bucket with a given name. Copy this name to the `COS_BUCKET_NAME` environment variable in the `.env` file you created in step 2. For the purposes of this starter kit, the bucket you create in Cloud Object Storage requires [public access](https://cloud.ibm.com/docs/services/cloud-object-storage/iam/public-access.html).
        * Copy the `apikey` and `iam_role_crn` values within the service credentials to the `COS_API_KEY` and `COS_IAM_ROLE_CRN` environment variables in the `.env` file you created in step 2.
        * Navigate to the `endpoints` URL within the service credentials (e.g. https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints) and choose a `public` `service-endpoint` that is close to your location. Copy your chosen endpoint to the `COS_ENDPOINT` environment variable in the `.env` file you created in step 2.

## 4. Install dependencies and run the applications

### Docker

```
docker build --tag video-transcriber:1.0 .
docker run --publish 3000:3000 --detach --name demo video-transcriber:1.0
```

### Server
1. This tutorial uses [pipenv](https://github.com/pypa/pipenv). If you are using another python distribution or package manager, you will need to install the dependencies located in the `Pipfile`. Alternatively, using pipenv, from the root project directory, create a pipenv virtual environment.
    ```bash
    pipenv --python <path to python executable>
    ```
    Note. If python 3.6 is installed in the default location, this can be specified as:
    ```bash
    pipenv --python 3.6
    ```
    
2. Activate the pipenv shell:
    ```bash
    pipenv shell
    ```
3. Install the project dependencies: 
    ```bash
    pipenv install
    ```
4. To run your application locally, use:  
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

### Frontend UI Development
1. If you have not done so already, install [`Node.js`](https://nodejs.org) and [`Yarn`](https://classic.yarnpkg.com/en/docs/install/).

2. In a new terminal, change to the `frontend` directory from the project root and install the dependencies:
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

## 5. Language Translator Extension
This tutorial shows you how to create a Watson Language Translator service and write the necessary server side code to translate video transcriptions. The front-end UI implementation is left as an extension for you to implement yourself. Hint - inspecting the `upload_video` function in `server/routes/index.py`, you can see that the server side expects a `source` and a `target` language as part of the POST request form data to `/upload_video`. Supported language models are provided at [https://localhost:3000/language_models](http://localhost:3000/language_models) once your server is running.

## 6. Deploy the app
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

Native application development was covered in step 4 above when you installed and ran the app. Your server is running at: `http://localhost:3000/` in your browser.

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
