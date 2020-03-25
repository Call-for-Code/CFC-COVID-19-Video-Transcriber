# Call for Code Video Transcriber Starter Kit

# Prerequisites

IBM Cloud account including:

1) IBM Watson Speech to Text Service
2) IBM Watson Language Translation Service
3) IBM Cloud Object Storage


# Setup
Create a `.env` file in the root project directory with the following environment variables:

```
IAM_AUTHENTICATOR_STT=<api key for speech to text service>
IAM_AUTHENTICATOR_TRANSLATE=<api key for translation service>
LANGUAGE_TRANSLATOR_SERVICE=<translator service endpoint. e.g. https://api.eu-gb.language-translator.watson.cloud.ibm.com>
COS_API_KEY_ID=<cloud object storage api key>
COS_RESOURCE_CRN=<cloud object storage resource crn. e.g. crn:v1:bluemix:public:iam::::serviceRole:Writer>
COS_AUTH_ENDPOINT=<cloud object storage auth endpoint. e.g. https://iam.cloud.ibm.com/identity/token>
COS_ENDPOINT=<cloud object storage endpoint. e.g. https://s3.eu-gb.cloud-object-storage.appdomain.cloud>
COS_BUCKET_NAME=<cloud object storage bucket name. e.g. transcripts>
```

# Running
* Install [Python](https://www.python.org/downloads/)
 
Running Flask applications has been simplified with a `manage.py` file to avoid dealing with configuring environment variables to run your app. From your project root, you can download the project dependencies with (NOTE: If you don't have pipenv installed, execute: `pip install pipenv`):

```bash
pipenv install
```

To run your application locally:

```bash
python manage.py start
```

`manage.py` offers a variety of different run commands to match the proper situation:
* `start`: starts a server in a production setting using `gunicorn`.
* `run`: starts a native Flask development server. This includes backend reloading upon file saves and the Werkzeug stack-trace debugger for diagnosing runtime failures in-browser.
* `livereload`: starts a development server via the `livereload` package. This includes backend reloading as well as dynamic frontend browser reloading. The Werkzeug stack-trace debugger will be disabled, so this is only recommended when working on frontend development.
* `debug`: starts a native Flask development server, but with the native reloader/tracer disabled. This leaves the debug port exposed to be attached to an IDE (such as PyCharm's `Attach to Local Process`).

There are also a few utility commands:
* `build`: compiles `.py` files within the project directory into `.pyc` files
* `test`: runs all unit tests inside of the project's `test` directory

Your application is running at: `http://localhost:3000/` in your browser. For more deployment options including deploying to IBM Cloud, please refer to the [deployment documentation](./Deployment.md).