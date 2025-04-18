<template>
  <div class="col-container gap-8">
    <div v-if="hasLoginToken" class="flex flex-col items-center w-full gap-4">
      <div class="flex w-full">
        <div class="flex w-full items-center justify-between gap-2">
            <span class="text-xl font-bold">🗺️ 나의 여행 일정</span>
            <router-link to="/travel/regist">
              <Button size="large" label="등록하기"/>
            </router-link>
        </div>
      </div>
      <table class="w-full border-table">
        <thead>
          <tr>
            <th class="al" style="width: 10%;">카테고리</th>
            <th class="al" style="width: 15%;">여행지</th>
            <th class="al" style="width: auto;">일정명</th>
            <th class="al" style="width: 250px;">기간</th>
            <th class="al" style="width: 8%;">인원수</th>
          </tr>
        </thead>
        <tbody class="hoverable">
            <tr>
              <td class="al">
                  <p>해외</p>
              </td>
              <td class="al">
                  <p>포르투갈, 암스테르담</p>
              </td>
              <td>
                  <p>나의 첫 유럽여행</p>
              </td>
              <td>
                  <p>2025-10-04 ~ 2025-10-14</p>
              </td>
              <td class="al">
                  <p>2명</p>
              </td>
            </tr>
            <tr>
              <td class="al">
                  <p>국내</p>
              </td>
              <td class="al">
                  <p>대한민국 > 통영</p>
              </td>
              <td>
                  <p>통영국제음악제</p>
              </td>
              <td>
                  <p>2025-03-29 ~ 2025-03-31</p>
              </td>
              <td class="al">
                  <p>2명</p>
              </td>
            </tr>
        </tbody>
      </table>
      <div class="flex w-full gap-2">
        <span>총</span><span class="font-bold" style="color: green;">2 건</span><span>의 데이터가 검색되었습니다.</span>
      </div>
      <Paginator :rows="10" :totalRecords="2"></Paginator>
    </div>


    <!-- old -->
    <div class="col-container gap-5" style="display: none;">
      <h1 class="text-xl">🗺️ 여행지를 검색해보세요!</h1>
      <h2 class="text-l">검색한 국가의 여행 정보를 확인해보세요. :)</h2>
      <InputGroup style="width: 25rem;">
          <InputText placeholder="Keyword" v-model="searchKeyword" @keyup.enter="searchLocation"/>
          <InputGroupAddon>
              <Button icon="pi pi-search" severity="secondary" variant="text" @click="searchLocation"/>
          </InputGroupAddon>
      </InputGroup>
      <div id="map" ref="mapContainer" class="map600"></div>
      <div id="map-detail" class="w-full h-full">
        <Tabs value="0" v-if="mapDetail">
          <TabList>
            <Tab value="0">기본 정보</Tab>
            <Tab value="1">상세 정보</Tab>
          </TabList>
          <TabPanels>
            <TabPanel value="0">
              <div v-if="mapDetail?.data?.basic">
                <DataTable :value="[mapDetail.data.basic]" showGridlines>
                  <Column v-for="col of mapDetail.data.basic" :key="col.field" :field="col.field" :header="col.header"></Column>
                </DataTable>
              </div>
              <div v-else>
                <p>데이터가 존재하지 않습니다.</p>
              </div>
            </TabPanel>
            <TabPanel value="1">
                <div v-if="mapDetail?.data?.details" class="flex flex-col ">
                  <Image src="https://blog.kakaocdn.net/dn/c6NGp8/btqFvuIRBXC/FdFwC4UMOZ49aNsDcJnvV1/img.jpg" alt="플러그 타입" class="col-container" style="width: 500px; height: auto;" />
                  <DataTable :value="[mapDetail.data.details]" showGridlines style="width: 500px; height: auto;">
                    <Column field="visaExemption" header="비자면제 여부"></Column>
                    <Column field="visaExemptionInfo" header="비자면제 정보"></Column>
                    <Column field="voltage" header="전압(V)"></Column>
                    <Column field="plugType" header="플러그"></Column>
                  </DataTable>
                  <p>* 위 데이터는 25.03.27 업데이트된 대한민국 공식 전자정부 누리집에서 가져왔습니다. (https://www.data.go.kr/data/15099235/fileData.do)</p>
                </div>
                <div v-else>
                  <p>데이터가 존재하지 않습니다.</p>
                </div>
            </TabPanel>
          </TabPanels>
        </Tabs>
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

    // 검색 결과에서 첫 번째 위치를 사용 (기본적으로 첫 번째 결과를 선택)
    const location = data[0];
    if (location) {
      const lat = location.lat;
      const lon = location.lon;

      if (!map.value) {
        console.warn("🚨 map이 아직 초기화되지 않았습니다!");
        return; // map이 초기화되지 않았다면 실행하지 않음
      }
      
      map.value.setView([lat, lon], 13);
      L.marker([lat, lon], { draggable: false })
        .addTo(map.value)
        .bindPopup("📍" + location.display_name)
        .openPopup();

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
    const countryCode = data.address.country_code.toUpperCase();

    // ✅ 상세 정보 초기화
    mapDetail.value = null;

    let countryInfoResponse = null;

    try {
      countryInfoResponse = await axios.get(`http://localhost:8081/api/map/searchCountry`, { params: { isoAlpha2: countryCode } });
    } catch (error) {
      console.error("🚨 국가 상세 정보 요청 오류:", error);
    }

    // ✅ 모든 데이터가 다 왔을 때만 mapDetail 업데이트
    mapDetail.value = countryInfoResponse.data;

    console.log('📘 국가 정보:', data);
    console.log('📘 국가 상세 정보:', countryInfoResponse.data);
  } catch (error) {
    console.error('Error fetching place details:', error);
  }
};
</script>