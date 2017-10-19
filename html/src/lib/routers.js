// 登录页
import Login from '../login.vue'
import App from '../App.vue'
import Analysis from '../Analysis.vue'
import Vieualization from '../visualization.vue'
export default function (router) {
  router.map({
    '/intellience': {name: 'App', component: App, subRoutes: {
      '/dashboard': {component: {template: '<router-view></router-view>'}, subRoutes: {
        '/analysis': {name: 'Analysis', component: Analysis, auth: true}
        // '/vieualization': {name: 'Vieualization', component: Vieualization, auth: true}
      }}
    }},
    '/login': {name: 'login', component: Login}
  })
  router.redirect({
    // '*': '/api/login'
  })
};
