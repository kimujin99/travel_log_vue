<template>
    <div class="w-full h-full flex flex-col justify-center items-center gap-8">
        <Panel header="어떤 나라를 여행하고 싶으신가요?" class="w-full h-full flex flex-col justify-center items-center gap-4">
            <Select v-model="selectedCity" editable :options="cities" optionLabel="name" placeholder="Select a City" class="w-full md:w-56" />
            <p class="m-0">
                내용
            </p>
        </Panel>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';

</script>