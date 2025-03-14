import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './styles/global.css';
import PrimeVue from "primevue/config";
import Aura from '@primeuix/themes/aura';
import 'primeicons/primeicons.css'

const app = createApp(App);

app
.use(router)
.use(PrimeVue, {
    // Default theme configuration
    theme: {
        preset: Aura,
        options: {
            prefix: 'p',
            darkModeSelector: false || 'none',
            cssLayer: false
        }
    }
 })
.mount('#app');