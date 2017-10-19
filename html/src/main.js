import Vue from 'vue'
import VueResource from 'vue-resource'
import VueRouter from 'vue-router'
import App from './App'
import RegisterRouters from './lib/routers'
// import Login from './login'

/* eslint-disable no-new */
new Vue({
  el: 'body',
  components: { App }
})
Vue.use(VueResource)
Vue.use(VueRouter)

var router = new VueRouter({
  hashbang: false,
  history: true,
  saveScrollPosition: true,
  transitionOnLoad: true
})

RegisterRouters(router)
router.start(App, '#app')
