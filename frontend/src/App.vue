<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/ibm-logo-white.png" class="logo">
    <Home />
  </div>
</template>

<script>
import Home from './components/Home.vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

export default {
  name: 'App',
  components: {
    Home
  }
}
</script>

<style>
html{
  background-color: #272D3B;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #fff;
  margin-top: 24px;
  background-color: #272D3B;
}
.logo {
  width: 120px;
  margin: 24px;
}
</style>
