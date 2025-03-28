<template>
  <div class="w-full h-full flex flex-col justify-center items-center gap-8">
    <div v-if="hasLoginToken" class="w-full h-full flex justify-center items-center" style="height: 150px;">
      <Button size="large" label="나의 여행 일정 등록하기"/>
    </div>
    <div class="w-full h-full flex justify-center flex-col items-center gap-5">
      <h1 class="text-xl">🗺️ 여행지를 검색해보세요!</h1>
      <h2 class="text-l">장소를 선택하면 리뷰와 평점을 확인할 수 있습니다. :)</h2>
      <InputGroup style="width: 25rem;">
          <InputText placeholder="Keyword" v-model="searchKeyword" @keyup.enter="handleSearch" />
          <InputGroupAddon>
              <Button icon="pi pi-search" severity="secondary" variant="text" @click="handleSearch" />
          </InputGroupAddon>
      </InputGroup>
      <div id="map"></div>
      <div id="map-details" v-if="hasSelectedPlace" class="mb-8 flex flex-col items-center justify-center w-full">
        <Panel :header="selectedPlace.name" class="w-full">
            <p class="m-0">
                {{ selectedPlace.formatted_address }}
            </p>
        </Panel>
        <div v-if="selectedPlace.photos || selectedPlace.reviews" class="flex items-center justify-center w-full">
          <div style="width: 50%; height: 350px;">
            <Galleria :value="photoUrls" :responsiveOptions="responsiveOptions" :numVisible="5" containerStyle="width: 100%; height: 350px; justify-content: center; align-items: center;">
                <template #item="slotProps">
                  <Image 
                    v-if="!errorMap[slotProps.item.src]"
                    :src="slotProps.item.src" 
                    alt="alt"
                    style="height: 250px; object-fit: contain;" 
                    @error="() => errorMap[slotProps.item.src] = true" 
                    preview
                  />
                  <img 
                    v-else
                    src="https://www.shoshinsha-design.com/wp-content/uploads/2020/05/noimage-760x460.png"
                    alt="fallback"
                    style="height: 250px; object-fit: contain;" 
                  />
                </template>
                <template #thumbnail="slotProps">
                  <div class="flex justify-center items-center">
                    <Image 
                      v-if="!errorMap[slotProps.item.src]"
                      :src="slotProps.item.src" 
                      alt="thumbnail" 
                      style="max-height: 99px; object-fit: cover;"
                      @error="() => errorMap[slotProps.item.src] = true"
                    />
                    <img 
                      v-else 
                      src="https://www.shoshinsha-design.com/wp-content/uploads/2020/05/noimage-760x460.png"
                      alt="thumbnail"
                      style="max-height: 99px; object-fit: cover;"
                    />
                  </div>
                </template>
            </Galleria>
          </div>
          <div style="width: 50%; height: 350px;">
            <ScrollPanel style="width: 100%; height: 350px;">
              <MainReviews v-for="(review, index) in selectedPlace.reviews" :key="index" :review="review" />
            </ScrollPanel>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import MainReviews from "./MainReviews.vue";

const googleMapsMapId = import.meta.env.VITE_GOOGLE_MAPS_MAP_ID;
let loginToken = ref(localStorage.getItem("authToken"));

let map;
let placesService;
let markers = [];
let searchKeyword = '';
let selectedPlace = ref({});
const errorMap = ref({});

//const image = "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";

const syncLoginState = () => {
    loginToken.value = localStorage.getItem("authToken");
};

// ✅ storage 이벤트 리스너 등록
onMounted(() => {
    window.addEventListener("storage", syncLoginState);
});

// ✅ 컴포넌트 unmount 될 때 정리
onBeforeUnmount(() => {
    window.removeEventListener("storage", syncLoginState);
});

const hasLoginToken = computed(() => {
  return loginToken.value && Object.keys(loginToken.value).length > 0;
});

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

  // ✅ 지도 클릭 이벤트 추가
  map.addListener("click", (event) => {
    const lat = event.latLng.lat();
    const lng = event.latLng.lng();
    searchPlaceByLatLng(lat, lng);  // 여기서 lat, lng를 전달
  });
}

// ✅ 검색 키워드로 장소 검색 (textSearch)
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

// ✅ 지도에서 클릭한 위치로 장소 검색 (textSearch)
function searchPlaceByLatLng(lat, lng) {
  const request = {
    query: `${lat}, ${lng}`,  // 클릭한 위치로 쿼리 생성
    fields: ["name", "geometry", "formatted_address", "photos", "reviews"]
  };

  placesService.textSearch(request, (results, status) => {
    if (status === google.maps.places.PlacesServiceStatus.OK && results.length > 0) {
      // ✅ 기존 데이터 삭제
      clearMarker();
      selectedPlace.value = {};

      const place = results[0];  // 첫 번째 검색 결과

      if (place.geometry?.location) {
        addMarker(place);
        searchPlaceDetails(place);
      }
    } else {
      console.warn("⚠️ 장소 검색 결과가 없습니다. 상태 코드:", status);
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