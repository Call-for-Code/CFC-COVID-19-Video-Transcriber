<template>
  <div>
      <b-container>
          <b-row>
              <b-col>
                <h1>Video Transcriber</h1>
              </b-col>
          </b-row>

          <b-row class="justify-content-md-center title-margin">
              <b-col cols="8">
                <p>This is a sample web app to transribe videos using IBM Watson Speech-to-Text API.</p>
                <h4>Instructions:</h4>
              </b-col>
          </b-row>

          <b-row class="justify-content-md-center">
              <b-col cols="8">
                <ol type="1" class="">
                    <li>Upload your video in mp4, mov, or avi format (max 50mb).</li>
                    <li>Wait for processing (may take up to 5 minutes).</li>
                    <li>Copy the output into your favorite word processing software.</li>
                </ol>
              </b-col>
          </b-row>

          <b-row>
            <b-col cols="8" class="mx-auto">
                <Upload class="title-margin"/>
            </b-col>
          </b-row>

          <b-row>
            <b-col cols="8" class="mx-auto">
              <Transcript v-bind:response="transcriptResponse"/>
            </b-col>
          </b-row>
      </b-container>
  </div>
</template>

<script>
import Upload from './Upload'
import Transcript from './Transcript'
import MqttClient from 'mqtt'

let transcriptResponse = ''

export default {
  name: 'Home',
  components: {
    Upload,
    Transcript
  },
  data() {
    return {
      mqttClient: null,
      transcriptResponse
    }
  },
  mounted: function() {
    this.mqttClient = MqttClient.connect('ws://test.mosquitto.org:8080')
    this.mqttClient.on('connect', () => {
      // console.log('MQTT client connected')
    })
  },
  methods: {
    subscribeToTopic(topic) {
      this.mqttClient.subscribe(topic)
      this.mqttClient.on('message', (topic, message) => {
        this.transcriptResponse = message.toString()
        // console.log('New message received')
        console.log(transcriptResponse)
      })
    }
  }
}
</script>

<style>
li, p, h4 {
    text-align: left;
}
body {
  background-color: #272D3B;
}
.title-margin {
    margin-top: 32px
}
</style>