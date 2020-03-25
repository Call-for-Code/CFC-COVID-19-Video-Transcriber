import time
from server import app
from moviepy.editor import *
from ibm_watson import SpeechToTextV1 
from ibm_watson.websocket import RecognizeCallback, AudioSource 

import json, os

AUDIO_BASE = os.path.dirname(os.getcwd()) + '/cfc-covid-19-video-transcriber-starter/server/'

def process_video(file_path, file_name, mqtt_topic):
    # Extract Audio
    app.config['MQTT_CLIENT'].publish(mqtt_topic, json.dumps({"msg_id": 0, "msg": "Extracting audio from video"}))
    print('0')
    video = VideoFileClip(file_path)    
    audio = video.audio

    app.config['MQTT_CLIENT'].publish(mqtt_topic, json.dumps({"msg_id": 1, "msg": "Saving audio file"}))
    print('1')
    audio_file = AUDIO_BASE+'/audio_extractions/'+file_name.split('.')[0]+'.mp3'
    audio.write_audiofile(audio_file)

    # Perform speech to text
    app.config['MQTT_CLIENT'].publish(mqtt_topic, json.dumps({"msg_id": 2, "msg": "Perfoming speech to text"}))
    print('2')
    with open(audio_file, 'rb') as audio_file: 
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
    print('3')
    while bool(dic.get('results')): 
        transcript = dic.get('results').pop().get('alternatives').pop().get('transcript')
    print(transcript) 
    app.config['MQTT_CLIENT'].publish(mqtt_topic, json.dumps({"msg_id": 4, "msg": transcript}))

    # Save results to cloud object storage

    # Delete video and audio files
