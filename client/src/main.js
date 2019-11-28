import 'bootstrap/dist/css/bootstrap.css';
import Vue from 'vue';
import axios from 'axios';
import App from './App.vue';
import router from './router';
import store from '../store/index';


axios.defaults.baseURL = 'http://localhost:5000';

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app');
