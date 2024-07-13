import { createApp } from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify'; // Import the vuetify instance
import 'vuetify/styles'; // Import Vuetify styles
import '@mdi/font/css/materialdesignicons.css'; // Import Material Design Icons
import router from './router'; // Import the router

const app = createApp(App);

app.use(vuetify);
app.use(router);

app.mount('#app');
