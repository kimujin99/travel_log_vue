<template>
    <Panel>
        <template #header>
            <div class="flex items-center gap-2">
                <Avatar :image="review.profile_photo_url" shape="circle" />
                <span class="font-bold">{{ review.author_name }}</span>
                <Rating :model-value="review.rating" :stars="5" readonly />
            </div>
        </template>
        <template #footer>
            <div class="flex flex-wrap items-center justify-between gap-4">
                <div class="flex items-center gap-2">
                </div>
                <span class="text-surface-500 dark:text-surface-400">{{ review.relative_time_description }}</span>
            </div>
        </template>
        <p class="m-0">{{ review.text }}</p>
    </Panel>
</template>

<script setup>

defineProps({
    review: Object // ✅ props로 데이터를 전달받음
});

</script>