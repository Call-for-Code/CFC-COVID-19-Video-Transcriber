import time
from server import app
from moviepy.editor import *
from ibm_watson import SpeechToTextV1 
from ibm_watson.websocket import RecognizeCallback, AudioSource 
from server.services.cos import multi_part_upload

import json, os

def process_video(file_path, file_name, mqtt_topic, source=None, target=None):
    # Extract Audio
    app.config['MQTT_CLIENT'].publish(mqtt_topic, json.dumps({"msg_id": 0, "msg": "Extracting audio from video"}))
    video = VideoFileClip(file_path)    
    audio = video.audio

    app.config['MQTT_CLIENT'].publish(mqtt_topic, json.dumps({"msg_id": 1, "msg": "Saving audio file"}))
    audio_file_path = os.path.join(app.config['AUDIO_FOLDER'],file_name.split('.')[0]+'.mp3')
    audio.write_audiofile(audio_file_path)

    # Perform speech to text
    app.config['MQTT_CLIENT'].publish(mqtt_topic, json.dumps({"msg_id": 2, "msg": "Perfoming speech to text"}))
    with open(audio_file_path, 'rb') as audio_file: 
        dic = json.loads( 
            json.dumps( 
                app.config['SPEECH_TO_TEXT'].recognize( 
                    audio=audio_file, 
                    content_type='audio/mp3', 
                    model='en-US_NarrowbandModel', 
                continuous=True).get_result(), indent=2
            )
        )  
    app.config['MQTT_CLIENT'].publish(mqtt_topic, json.dumps({"msg_id": 3, "msg": "Extracting transcript"}))
    while bool(dic.get('results')): 
        transcript = dic.get('results').pop().get('alternatives').pop().get('transcript')
    print(transcript) 
    app.config['MQTT_CLIENT'].publish(mqtt_topic, json.dumps({"msg_id": 4, "msg": "Transcript extracted", "body": transcript}))

    # Translate if necessary
    if source is not None and target is not None:
        model_id = source+'-'+target
        app.config['MQTT_CLIENT'].publish(mqtt_topic, json.dumps({"msg_id": 5, "msg": "Translating..."}))
        transcript = app.config['LANGUAGE_TRANSLATOR'].translate(text=transcript, model_id=model_id).get_result()
        transcript = json.dumps(transcript["translations"][0]["translation"], indent=2, ensure_ascii=False)
        app.config['MQTT_CLIENT'].publish(mqtt_topic, json.dumps({"msg_id": 6, "msg": "Transcript translated", "body": transcript}))

    # Save results to cloud object storage
    app.config['MQTT_CLIENT'].publish(mqtt_topic, json.dumps({"msg_id": 7, "msg": "Saving results to cloud object storage"}))
    output_file = file_name.split('.')[0]+'.txt'
    output_path = os.path.join(app.config['OUTPUT_FOLDER'],output_file)
    f = open(output_path, "w")
    f.write(transcript)
    f.close()
  
    multi_part_upload(app.config['COS_BUCKET_NAME'], output_file, output_path)

    # Build URL
    url = 'https://' + app.config['COS_BUCKET_NAME'] +'.'+app.config['COS_ENDPOINT'].split('//')[1]+'/'+output_file
    app.config['MQTT_CLIENT'].publish(mqtt_topic, json.dumps({"msg_id": 8, "msg": "Upload complete", "url": url}))

    # Delete video, audio and transcript files
    os.remove(file_path)
    os.remove(audio_file_path)
    os.remove(output_path)
