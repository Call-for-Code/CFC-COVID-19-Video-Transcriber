<template>
  <div>
      <b-row class="mt-5">
          <b-col cols="3">
            <h3>Transcription</h3>
          </b-col>
          <b-col cols="9" class="text-right">
            <img src="../assets/powered-by-watson.png" alt="">
          </b-col>
      </b-row>
      <b-row class="pl-3 pr-3">
          <b-col class="transcript-container">
              <samp>{{ response }}</samp>
          </b-col>
      </b-row>
  </div>
</template>

<script>
export default {
  name: 'Transcript',
  props: ['response']
}
</script>

<style>
.transcript-container {
    margin-top: 24px;
    background-color: #000;
    border-radius: 8px;
    padding: 24px;
}
</style>