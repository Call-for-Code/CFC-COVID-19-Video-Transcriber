<template>
    <div>
        <vue-dropzone ref="myVueDropzone" id="dropzone" :options="dropzoneOptions" @vdropzone-success="fileUploaded"></vue-dropzone>
    </div>
</template>

<script>
import vue2Dropzone from 'vue2-dropzone'
import 'vue2-dropzone/dist/vue2Dropzone.min.css'

export default {
  name: 'Upload',
  components: {
    vueDropzone: vue2Dropzone
  },
  data: () => {
    return {
      dropzoneOptions: {
          url: 'http://localhost:3000/upload_video',
          thumbnailWidth: 200,
          maxFilesize: 50.0,
          headers: { "My-Awesome-Header": "header value" },
          dictDefaultMessage: "<b-icon-arrow-up></b-icon-arrow-up><h3>Drop a video here to upload</h3><img src='./upload.png' class='upload-icon'/>"
      }
    }
  },
  methods: {
    fileUploaded(file, response) {
      console.log(response)
      this.$parent.subscribeToTopic(response.mqtt_topic)
    }
  }
}
</script>

<style>
.dropzone {
    background-color: #000;
    border-radius: 8px;
    height: 400px;
}
.vue-dropzone {
    border: none;
    color: rgb(193, 193, 193);
}
.upload-icon {
    width:96px;
    margin-top: 80px
}
</style>

