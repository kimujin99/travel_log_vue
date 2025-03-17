<template>
  <div class="w-full h-full flex flex-col items-center gap-4">
    <h1 class="text-xl">여행지를 검색해보세요.</h1>
    <InputGroup style="width: 25rem;">
        <InputText placeholder="Keyword"/>
        <InputGroupAddon>
            <Button icon="pi pi-search" severity="secondary" variant="text"/>
        </InputGroupAddon>
    </InputGroup>
    <div id="map" style="width: 100%; height: 600px;"></div>
  </div>
</template>

<script>
let map;

export default {
  name: 'Main',
  mounted() {
    this.initMap();
  },
  methods: {
    async initMap() {
      if (typeof google === 'undefined' || !google.maps) {
        console.error("Google Maps API가 로드되지 않았습니다.");
        return;
      }

      const { Map } = await google.maps.importLibrary("maps");

      new Map(document.getElementById("map"), {
        center: { lat: 37.564, lng: 127.001 },
        zoom: 8,
      });
    }
  },
}
</script>