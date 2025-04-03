<template>
  <div class="col-container gap-8">
    <div v-if="hasLoginToken" class="row-container" style="height: 150px;">
      <router-link to="/travle/regist">
        <Button size="large" label="나의 여행 일정 등록하기"/>
      </router-link>
    </div>
    <div class="col-container gap-5">
      <h1 class="text-xl">🗺️ 여행지를 검색해보세요!</h1>
      <h2 class="text-l">검색한 국가의 여행 정보를 확인해보세요. :)</h2>
      <InputGroup style="width: 25rem;">
          <InputText placeholder="Keyword" v-model="searchKeyword" @keyup.enter="searchLocation"/>
          <InputGroupAddon>
              <Button icon="pi pi-search" severity="secondary" variant="text" @click="searchLocation"/>
          </InputGroupAddon>
      </InputGroup>
      <div id="map" ref="mapContainer"></div>
      <div id="map-detail" v-if="hasMapDetail" class="w-full h-full">
        <Panel :header="mapDetail.koreanName + '(' + mapDetail.englishName + ')'" :headerStyle="{ fontSize: '2rem' }">
            <div class="row-container">
              <div class="col-container">
                <span class="material-symbols-outlined">
                  public
                </span>
                <p class="font-bold">국가코드</p>
                <p>{{ mapDetail.isoAlpha2 }} / {{ mapDetail.isoAlpha3 }}</p>
              </div>
              <div class="col-container">
                <span class="material-symbols-outlined">
                  airplane_ticket
                </span>
                <p class="font-bold">비자</p>
                <p>{{ mapDetail.visaRequirement }}</p>
              </div>
              <div class="col-container">
                <span class="material-symbols-outlined">
                  offline_bolt
                </span>
                <p class="font-bold">전압</p>
                <p>{{ mapDetail.voltage }}V</p>
              </div>
            </div>
        </Panel>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const loginToken = ref(localStorage.getItem("authToken"));
const map = ref(null);
const mapContainer = ref(null);
const mapDetail = ref(null);
const searchKeyword = ref('');


// ✅ 로그인 여부 확인
const syncLoginState = () => {
    loginToken.value = localStorage.getItem("authToken");
};

onMounted(() => {
    window.addEventListener("storage", syncLoginState);
});

onBeforeUnmount(() => {
    window.removeEventListener("storage", syncLoginState);
});

const hasLoginToken = computed(() => {
  return loginToken.value && Object.keys(loginToken.value).length > 0;
});

const hasMapDetail = computed(() => {
  return mapDetail.value && Object.keys(mapDetail.value).length > 0;
});

// ✅ 지도 출력
onMounted(() => {
  if (!mapContainer.value) return;

  map.value = L.map('map').setView({ lon: 0, lat: 0 }, 2); // map 객체를 ref에 저장

  map.value.setMaxBounds([[-90, -180], [90, 180]]); // 최대 이동 범위 설정
  map.value.setMinZoom(2); // 최소 줌 아웃 수준
  map.value.setMaxZoom(19); // 최대 줌 인 수준

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap 기여자</a>',
  }).addTo(map.value);

  // 축척 막대를 지도 왼쪽 하단에 노출
  L.control.scale({ imperial: true, metric: true }).addTo(map.value);
});

// ✅ Nominatim API로 장소 검색하는 함수
const searchLocation = async () => {
  if (!searchKeyword.value) return;

  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?q=${searchKeyword.value}&format=json&limit=5`
    );
    const data = await response.json();

    removeAllMarkers(); // 마커 초기화

    console.log(data);

    // 검색 결과에서 첫 번째 위치를 사용 (기본적으로 첫 번째 결과를 선택)
    const location = data[0];
    if (location) {
      const lat = location.lat;
      const lon = location.lon;

      if (!map.value) return; // map이 초기화되지 않았다면 실행하지 않음
      
      map.value.setView([lat, lon], 13);
      L.marker([lat, lon], { draggable: false }).addTo(map.value).bindPopup(location.display_name).openPopup();

      getCountryCode(lat, lon);
    } else {
      alert('🚨 검색 결과가 존재하지 않습니다!');
    }
  } catch (error) {
    console.error('Error fetching location:', error);
  }
};

// ✅ 기존 마커 제거하는 함수
const removeAllMarkers = () => {
  if (!map.value) return;
  map.value.eachLayer(layer => {
    if (layer instanceof L.Marker) {
      map.value.removeLayer(layer);
    }
  });
};

const getCountryCode = async (lat, lon) => {
  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`
    );
    const data = await response.json();

    getCountryInfo(data.address.country_code.toUpperCase());

    console.log('상세 정보:', data.address.country_code.toUpperCase()); // 🔥 가져온 데이터 확인
  } catch (error) {
    console.error('Error fetching place details:', error);
  }
};

const getCountryInfo = async (code) => {
  try {
    // 국가 상세 정보보 API 요청
    const response = await axios.get(`http://localhost:8081/api/map/searchCountry`, {
      params: { isoAlpha2: code },
    });

    mapDetail.value = response.data;

    console.log('상세 정보:', response); // 🔥 가져온 데이터 확인
  } catch (error) {
    // 오류 처리
    console.log("🔥 ERROR_STATUS : ", error.response?.status);
    console.log("🔥 ERROR_DATA : ", error.response?.data);
    console.log("🔥 ERROR_MESSAGE : ", error.message);
  }
};
</script>