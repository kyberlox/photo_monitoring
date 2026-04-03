<template>
<div class="mt-5">
    <div v-if="!activeMarker"
         class="text-lg ">Выберите точку на карте</div>
    <div class="px-4 left text-lg">
        {{ activeMarker?.name }}
    </div>
</div>
<div class="flex flex-col mt-5 border-gray-50 bg-gray-50 border p-2 rounded-md"
     v-for="(image, index) in activeMarker?.photos"
     :key="index + 'img'"
     @click="{ activeImage = 'src/assets/img/test.jpg'; visibleModal = true }">
    <img class="object-cover rounded-sm w-full h-full mt-2  cursor-pointer hover:scale-101 transition duration-200"
         :src="image.file_url" />
</div>
<FileLoader v-if="activeMarker"
            :coordinates="(activeMarker?.coordinates as LngLat)"
            :name="activeMarker?.name"
            @addNewPoint="(data) => $emit('updatePhoto', data)" />
<SlotModal v-if="activeImage && visibleModal"
           @close="visibleModal = false">
    <img class="object-contain w-full h-full"
         :src="activeImage" />
</SlotModal>
</template>
<script lang="ts">
import { defineComponent, ref, type PropType } from 'vue';
import SlotModal from './layout/SlotModal.vue';
import type { IMapMarker } from '@/interfaces/IMapMarkers';
import FileLoader from './common/FileLoader.vue';
import type { LngLat } from '@yandex/ymaps3-types';

export default defineComponent({
    components: { SlotModal, FileLoader },
    emits: ['updatePhoto'],
    props: {
        activeMarker: {
            type: Object as PropType<IMapMarker>
        },
    },
    setup() {
        const activeImage = ref<string>();
        const visibleModal = ref(false);

        return {
            activeImage,
            visibleModal
        }
    }
})
</script>