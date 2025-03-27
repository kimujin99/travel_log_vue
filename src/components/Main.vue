<template>
  <div class="w-full h-full flex flex-col items-center gap-5">
    <h1 class="text-xl">여행지를 검색해보세요.</h1>
    <InputGroup style="width: 25rem;">
        <InputText placeholder="Keyword" v-model="searchKeyword" @keyup.enter="handleSearch" />
        <InputGroupAddon>
            <Button icon="pi pi-search" severity="secondary" variant="text" @click="handleSearch" />
        </InputGroupAddon>
    </InputGroup>
    <div id="map"></div>
    <div id="map-details" v-if="hasSelectedPlace" class="mb-8 flex flex-col items-center justify-center">
      <Panel :header="selectedPlace.name" class="w-full">
          <p class="m-0">
              {{ selectedPlace.formatted_address }}
          </p>
      </Panel>
      <div class="flex items-center justify-center">
        <Galleria v-if="photoUrls.length > 0" :value="photoUrls" :responsiveOptions="responsiveOptions" :numVisible="5" containerStyle="width: 50%; height: 350px;">
            <template #item="slotProps">
                <img :src="slotProps.item.src" alt="alt" style="width: 100%; max-height: 250px; object-fit: contain;" @error="onImageError" />
            </template>
            <template #thumbnail="slotProps">
                <img :src="slotProps.item.src" alt="thumbnail-alt" style="max-height: 100px; object-fit: cover;" @error="onImageError" />
            </template>
        </Galleria>
        <ScrollPanel style="width: 50%; height: 350px;">
          <MainReviews v-for="(review, index) in selectedPlace.reviews" :key="index" :review="review" />
        </ScrollPanel>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import MainReviews from "./MainReviews.vue";

const googleMapsMapId = import.meta.env.VITE_GOOGLE_MAPS_MAP_ID;
let map;
let placesService;
let markers = [];
let searchKeyword = '';
let selectedPlace = ref({});
//const image = "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";

const hasSelectedPlace = computed(() => {
  return selectedPlace.value && Object.keys(selectedPlace.value).length > 0;
});

const photoUrls = computed(() => {
  return selectedPlace.value.photos?.map(photo => ({
    src: photo.getUrl({ maxHeight: 350 }) // Google API에서 URL 변환
  }));
});

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
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 37.5665, lng: 126.9780 }, // 서울 좌표
    zoom: 10,
    mapId: googleMapsMapId,
    //disableDefaultUI: true, // ✅ 기본 UI 전체 비활성화
    mapTypeControl: false,  // ✅ 지도 유형(위성 지도 등) 선택 버튼 비활성화
    streetViewControl: false, // ✅ 거리뷰 아이콘 비활성화
  });

  // placesService 초기화
  placesService = new google.maps.places.PlacesService(map);
}

function searchPlaces(keyword) {
  if (!placesService || !keyword) return;
  
  const request = {
    query: keyword,
    fields: ["name", "geometry", "formatted_address"],
  };

  placesService.textSearch(request, (results, status) => {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
      // ✅ 기존 데이터 삭제
      clearMarker();
      selectedPlace.value = {};

      results.forEach((place) => {
        if (place.geometry?.location) {
          addMarker(place); // ✅ 새 마커 추가
        }
      });
    }
  });
}

function addMarker(place) {
  const marker = new google.maps.Marker({
    position: place.geometry.location,
    map: map,
    //icon: image,
    title: place.name,
  });

  marker.place_id = place.place_id;

  // ✅ 마커 클릭 이벤트 추가
  marker.addListener("click", function () {
    searchPlaceDetails(this);
  });
  
  map.setCenter(place.geometry.location); // ✅ 검색 후 항상 마커를 중심으로 지도 이동
  map.setZoom(14); // ✅ 검색 후 항상 줌을 14로 설정

  markers.push(marker);
}

function clearMarker() {
  markers.forEach((marker, index) => {
    if (marker.getMap()) {
      marker.setMap(null);
    }
  });

  markers = [];
}

function handleSearch() {
  if (searchKeyword) {
    searchPlaces(searchKeyword);
  }
}

async function searchPlaceDetails(marker) {
  if (!placesService || !marker || !marker.place_id) return;

  const request = {
    placeId: marker.place_id,
    fields: ["name", "formatted_address", "geometry", "reviews", "photos"], // ✅ 필요한 필드 지정
  };

  placesService.getDetails(request, (place, status) => {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
      selectedPlace.value = place;

      console.log("장소 정보:", place);
    } else {
      console.error("🚨 장소 정보를 가져오는 데 실패했습니다! :", status);
    }
  });
}

// ✅ 이미지 로드 실패 시 대체 이미지로 변경
function onImageError(event) {
  event.target.src = "https://www.shoshinsha-design.com/wp-content/uploads/2020/05/noimage-760x460.png";
}

</script>