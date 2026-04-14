<template>
<div class="mt-5 w-full">
    <div v-if="!activeMarker?.coordinates"
         class="text-lg ">Выберите точку на карте</div>
    <div class="px-4 left text-lg">
        {{ activeMarker?.name }}
    </div>
    <div class="px-4 left text-lg">
        {{ activeMarker?.coordinates }}
    </div>
</div>
<div class="flex flex-col mt-5 border-gray-50 bg-gray-50 border p-2 rounded-md w-full"
     v-for="(image, index) in activeMarker?.photos"
     :key="index + 'img'">
    <img class="object-cover rounded-sm w-full mt-2 cursor-pointer hover:scale-101 transition duration-200 max-h-[500px]"
         :src="image.file_url"
         @click="{ activeImage = image.file_url; visibleModal = true }" />
    <span class="text-sm underline text-red-600 hover:text-red-400 cursor-pointer"
          @click="$emit('deletePhoto', image.id)">Удалить</span>
</div>
<FileLoader v-if="activeMarker?.coordinates"
            :coordinates="(activeMarker?.coordinates as LngLat)"
            :name="activeMarker?.name"
            @addNewPoint="(data) => $emit('updatePhoto', data)" />
<SlotModal v-if="activeImage && visibleModal"
           @close="visibleModal = false">
    <img class="object-contain w-full h-full max-h-[90vh]"
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
    emits: ['updatePhoto', 'deletePhoto'],
    props: {
        activeMarker: {
            type: Object as PropType<IMapMarker | null>
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