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
</script>