<template>

  <div class="inquire_input">
    <div >
      <label>用户名:</label><input id="username" v-model="username" placeholder="username">
      <label>密码:</label><input id="password" v-model="password" placeholder="password">
      <button @click="login()">登录</button>
    </div>
  </div>

</template>
<style>
  .inquire_input{
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
  }

</style>
<script>
    export default{
      data () {
        return {
          username: '',
          password: ''
        }
      },
      methods: {
        login () {
          let data = {
            action: 'my_login',
            username: this.username,
            password: this.password
          }
          this.$http.post('/api/login/', data, {emulateJSON: true}).then(function (response) {
            if (response.status === 200) {
              console.log('login')
              window.localStorage.setItem('user_id', response.data.data.user_id)
              this.$router.go({name: 'Analysis'})
            }
          })
        }
      }
    }
</script>
