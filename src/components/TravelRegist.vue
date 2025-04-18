<template>
    <Form @submit="save" class="flex flex-col items-center w-full gap-4">
        <div class="flex w-full p-2"><span class="text-xl font-bold">여행 일정 등록</span></div>
        <table class="w-full border-table">
            <tbody>
                <tr>
                    <th class="al" style="width: 200px;">일정명</th>
                    <td>
                        <InputText type="text" v-model="value" class="w-full"/>
                    </td>
                </tr>
                <tr>
                    <th class="al">분류</th>
                    <td>
                        <Select v-model="value1" :options="cities" placeholder="선택" class="w-60"/>
                    </td>
                </tr>
                <tr>
                    <th class="al">여행 국가</th>
                    <td>
                        <Select v-model="value1" :options="cities" placeholder="선택" class="w-60"/>
                    </td>
                </tr>
                <tr>
                    <th class="al">여행 기간</th>
                    <td>
                        <div class="flex items-center gap-1">
                            <DatePicker v-model="value3" size="Normal" placeholder="출발일" showIcon iconDisplay="input" class="mr-2"/>
                            <span class="mr-2">~</span>
                            <DatePicker v-model="value3" size="Normal" placeholder="도착일" showIcon iconDisplay="input" />
                        </div>
                    </td>
                </tr>
                <tr>
                    <th class="al">내용</th>
                    <td>
                        <Textarea v-model="value" autoResize rows="10" class="w-full"/>
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="flex justify-center items-center gap-2">
            <router-link to="/">
                <Button size="large" severity="info" label="목록"/>
            </router-link>
            <Button size="large" label="등록하기"/>
        </div>
    </Form>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// const map = ref(null);
// const mapContainer = ref(null);

// // ✅ 지도 출력
// onMounted(() => {
//   if (!mapContainer.value) return;

//   map.value = L.map(mapContainer.value, {
//     center: [37.5665, 126.9780], // 📌 서울 좌표
//     zoom: 6, 
//     dragging: false, // ✅ 드래그 비활성화
//     scrollWheelZoom: false, // ✅ 마우스 휠 줌 비활성화
//     doubleClickZoom: false, // ✅ 더블 클릭 줌 비활성화
//     touchZoom: false, // ✅ 터치 줌 비활성화
//     boxZoom: false, // ✅ 드래그 박스 줌 비활성화
//     keyboard: false, // ✅ 키보드 컨트롤 비활성화
//     zoomControl: false // ✅ 기본 줌 컨트롤 UI 제거
//   });

//   L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     maxZoom: 19,
//     attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap 기여자</a>',
//   }).addTo(map.value);

//     // ✅ 서울(한국 중앙)에 마커 추가
//     L.marker([37.5665, 126.9780], { draggable: false })
//     .addTo(map.value)
//     .bindPopup("📍 서울 (Seoul)")
//     .openPopup();
// });
</script>