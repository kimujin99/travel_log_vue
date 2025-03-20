<template>
  <div id="app" class="app-container">
    <Header />
    <div class="main-container">
      <router-view />
    </div>
    <Footer />
  </div>
</template>

<script setup>
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import { onMounted } from 'vue';

const googleMapsApiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

onMounted(() => {
  if (!googleMapsApiKey) {
    console.error("🚨 API 키가 존재하지 않습니다!");
    return;
  }

// Google Maps API 로드가 완료될 때까지 기다리는 Promise 생성
window.googleMapsReady = new Promise((resolve) => {
  window.initMap = () => {
    resolve();
  };
});

  // Google Maps API 스크립트 로드
  const script = document.createElement('script');
  script.src = `https://maps.googleapis.com/maps/api/js?key=${googleMapsApiKey}&callback=initMap`;
  script.async = true;
  script.defer = true;
  document.head.appendChild(script);
});
</script>