<template>
  <div id="main_div" style="height:100%;">

    <router-view></router-view>

    <!--<div class="inquire_input">-->
      <!--<input id="inquire_ask" v-model="message" placeholder="edit me">-->
      <!--<button @click="inquire()">分析</button>-->
    <!--</div>-->
  </div>
</template>

<script>
export default {
  data () {
    return {
      message: ''
    }
  },
  methods: {
    ready () {
      this.message = ''
    },
    inquire () {
      let data = {
        'domain': this.message
      }
      this.$http.post('/api/', data).then(function (response) {
        if (response.status === 200) {
          console.log(this.message)
        }
      }, function (response) {

      })
    }
  },
  components: {
  }
}
</script>

<style>
html {
  height: 100%;
}

body {
  height: 100%;
  background: url("./assets/bg.jpg") no-repeat;
  background-size: cover;
}

#app {
  color: #2c3e50;
  margin-top: -100px;
  max-width: 600px;
  font-family: Source Sans Pro, Helvetica, sans-serif;
  text-align: center;
}

#app a {
  color: #42b983;
  text-decoration: none;
}
</style>
