<template>
  <div class="w-full h-full flex flex-col items-center gap-5">
    <h1 class="text-xl">여행지를 검색해보세요.</h1>
    <InputGroup style="width: 25rem;">
        <InputText placeholder="Keyword"/>
        <InputGroupAddon>
            <Button icon="pi pi-search" severity="secondary" variant="text"/>
        </InputGroupAddon>
    </InputGroup>
    <div id="map"></div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';

const googleMapsMapId = import.meta.env.VITE_GOOGLE_MAPS_MAP_ID;

onMounted(async () => {
  if (!window.googleMapsReady || !googleMapsMapId) {
    console.error("🚨 Google Maps API가 로드되지 않았습니다!");
    return;
  }

  // ✅ Google Maps API가 로드될 때까지 기다림
  await window.googleMapsReady;
  initMap();
});

function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 37.5665, lng: 126.9780 }, // 서울 좌표 예시
    zoom: 10,
    mapId: googleMapsMapId,
    disableDefaultUI: true, // ✅ 기본 UI 전체 비활성화
    mapTypeControl: false,  // ✅ 지도 유형(위성 지도 등) 선택 버튼 비활성화
    streetViewControl: false, // ✅ 거리뷰 아이콘 비활성화
  });
}
</script>