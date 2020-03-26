from server import app
from flask import render_template, flash, jsonify, request, redirect
from threading import Thread
from server.tasks import process_video

import os, uuid

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mpeg', 'mov', 'm4v'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

@app.route("/language_models", methods=['GET'])
def language_models():
    models = app.config['LANGUAGE_TRANSLATOR'].list_models().get_result()
    languages = app.config['LANGUAGE_TRANSLATOR'].list_identifiable_languages().get_result()
    return jsonify({"models": models["models"], "languages": languages["languages"]})

@app.route("/upload_video", methods=['POST'])
def upload_video():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part. Please ensure the video is uploaded as multipart form data with the key as 'file'."}), 400
    file = request.files['file']
   
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        file_id = str(uuid.uuid1())
        mqtt_topic = 'cfc-covid-19-video-transcriber-starter/'+ file_id
        new_filename = file_id + '.'+ file.filename.split('.')[1]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(file_path)

        # extract translation fields if specified
        source = None
        target = None
        form_fields = request.form.to_dict(flat=False)
        if 'source' in form_fields and 'target' in form_fields:
            source = form_fields['source'][0]
            target = form_fields['target'][0]

        # start pipeline as a new thread
        thread = Thread(target=process_video, args=(file_path,new_filename,mqtt_topic,source,target,))
        thread.daemon = True
        thread.start()

        # return mqtt namespace for listening for video updates
        return jsonify({"msg": "file uploaded", "mqtt_topic": mqtt_topic})
    else:
        return jsonify({"error": "File must be one of: "+json.dumps(ALLOWED_EXTENSIONS)}), 400


@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return app.send_static_file('404.html')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return app.send_static_file('500.html')
