import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createYmaps } from 'vue-yandex-maps';

import App from './App.vue'

const app = createApp(App)

app
.use(createPinia())
.use(createYmaps({
  apikey: '3f8f0af1-723b-47db-b868-be798083bba6',
}));

app.mount('#app')