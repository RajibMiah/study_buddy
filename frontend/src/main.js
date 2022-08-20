
import { createApp } from 'vue';
import App from './App.vue';
import './assets/main.css';
import router from "./router/index";
import store from "./store";
import './styles/main.scss';


import "../node_modules/bootstrap/dist/css/bootstrap.css";
import "../node_modules/bootstrap/dist/js/bootstrap.bundle";

// global.jQuery = require('jquery');
// var $ = global.jQuery;
// window.$ = $;

createApp(App).use(store).use(router).mount('#app')
