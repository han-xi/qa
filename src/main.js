
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css';

import auth from './auth/index'
const app = createApp(App)
app.use(router)
app.use(Antd)
auth.checkAuth();
app.mount('#app')