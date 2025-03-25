<template>
  <div class="w-full h-full flex flex-col items-center gap-5">
    <h1 class="text-xl">여행지를 검색해보세요.</h1>
    <InputGroup style="width: 25rem;">
        <InputText placeholder="Keyword" v-model="searchKeyword" @keyup.enter="handleSearch" />
        <InputGroupAddon>
            <Button icon="pi pi-search" severity="secondary" variant="text" @click="handleSearch"/>
        </InputGroupAddon>
    </InputGroup>
    <div id="map"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const googleMapsMapId = import.meta.env.VITE_GOOGLE_MAPS_MAP_ID;
const map = ref(null);
const placesService = ref(null);
const markers = ref([]);
const searchKeyword = ref('');
const image = "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";

onMounted(async () => {
  if (!window.googleMapsReady) {
    console.error("🚨 Google Maps API가 로드되지 않았습니다!");
    return;
  }

  // ✅ Google Maps API가 로드될 때까지 기다림
  await window.googleMapsReady;

  initMap();
});

function initMap() {
  map.value = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 37.5665, lng: 126.9780 }, // 서울 좌표 예시
    zoom: 10,
    mapId: googleMapsMapId,
    disableDefaultUI: true, // ✅ 기본 UI 전체 비활성화
    mapTypeControl: false,  // ✅ 지도 유형(위성 지도 등) 선택 버튼 비활성화
    streetViewControl: false, // ✅ 거리뷰 아이콘 비활성화
  });

  // placesService 초기화
  placesService.value = new google.maps.places.PlacesService(map.value);
}

function searchPlaces(keyword) {
  if (!placesService.value || !keyword) return;
  
  const request = {
    query: keyword,
    fields: ["name", "geometry", "formatted_address"],
  };

  placesService.value.textSearch(request, (results, status) => {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
      clearMarkers();
      results.forEach((place) => {
        if (place.geometry?.location) {
          addMarker(place);
        }
      });
    }
  });
}

function addMarker(place) {
  const marker = new google.maps.Marker({
    position: place.geometry.location,
    map: map.value,
    icon: image,
    title: place.name,
  });
  // 마커를 중심으로 지도 이동
  map.value.setCenter(place.geometry.location);
  markers.value.push(marker);
}

function clearMarkers() {
  console.log("삭제할 마커 수:", markers.value.length); // 마커 수 확인
  markers.value.forEach((marker, index) => {
    if (marker.getMap()) {
      console.log(`마커 ${index} 제거:`, marker);
      marker.setMap(null); // 마커를 지도에서 제거
    }
  });
  markers.value = [];
  console.log("마커 배열 초기화 완료:", markers.value); // 배열 초기화 확인
}

function handleSearch() {
  if (searchKeyword.value) {
    searchPlaces(searchKeyword.value);
  }
}

</script>