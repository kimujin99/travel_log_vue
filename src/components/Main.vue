<template>
  <div class="w-full h-full flex flex-col items-center gap-4">
    <h1 class="text-xl">여행지를 검색해보세요.</h1>
    <InputGroup style="width: 25rem;">
        <InputText placeholder="Keyword"/>
        <InputGroupAddon>
            <Button icon="pi pi-search" severity="secondary" variant="text"/>
        </InputGroupAddon>
    </InputGroup>
  </div>
</template>

<script>
export default {
  name: 'Main'
}
</script>