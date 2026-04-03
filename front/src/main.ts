import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createYmaps } from 'vue-yandex-maps';

import App from './App.vue'

const app = createApp(App)

app
.use(createPinia())
.use(createYmaps({
  apikey: '44cd4d19-a17e-41a7-8855-f2e0cddba206',
}));

app.mount('#app')