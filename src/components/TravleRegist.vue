<template>
    <div class="row-container" style="align-items: stretch;">
        <div id="map" ref="mapContainer" class="map500"></div>
        <div class="flex flex-col w-full h-full ml-8 gap-6">
            <div class="flex flex-col w-full">
                <label for="value1" class="font-bold block mb-2"> 1. 여행 제목을 입력하세요. </label>
                <div class="flex items-center gap-1">
                    <InputText type="text" v-model="value" class="w-90"/>
                </div>
            </div>
            <div class="flex flex-col w-full">
                <label for="value1" class="font-bold block mb-2"> 2. 여행 지역을 선택하세요. </label>
                <div class="flex gap-2">
                    <Select v-model="value1" :options="cities" placeholder="국가명" class="w-60"/>
                    <Select v-model="value2" :options="cities" placeholder="도시명" class="w-60"/>
                </div>
            </div>
            <div class="flex flex-col w-full">
                <label for="value1" class="font-bold block mb-2"> 3. 여행 일정을 입력하세요. </label>
                <div class="flex items-center gap-1">
                    <DatePicker v-model="value3" size="Normal" placeholder="출발일" showIcon iconDisplay="input" class="mr-2"/>
                    <span class="mr-2">~</span>
                    <DatePicker v-model="value3" size="Normal" placeholder="도착일" showIcon iconDisplay="input" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const map = ref(null);
const mapContainer = ref(null);

// ✅ 지도 출력
onMounted(() => {
  if (!mapContainer.value) return;

  map.value = L.map(mapContainer.value, {
    center: [37.5665, 126.9780], // 📌 서울 좌표
    zoom: 6, 
    dragging: false, // ✅ 드래그 비활성화
    scrollWheelZoom: false, // ✅ 마우스 휠 줌 비활성화
    doubleClickZoom: false, // ✅ 더블 클릭 줌 비활성화
    touchZoom: false, // ✅ 터치 줌 비활성화
    boxZoom: false, // ✅ 드래그 박스 줌 비활성화
    keyboard: false, // ✅ 키보드 컨트롤 비활성화
    zoomControl: false // ✅ 기본 줌 컨트롤 UI 제거
  });

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap 기여자</a>',
  }).addTo(map.value);

    // ✅ 서울(한국 중앙)에 마커 추가
    L.marker([37.5665, 126.9780], { draggable: false })
    .addTo(map.value)
    .bindPopup("📍 서울 (Seoul)")
    .openPopup();
});
</script>