<template>
<div class="m-5 left text-lg">{{ activeMarker?.name }}</div>
<div class="flex flex-col mt-5 border-gray-50 bg-gray-50 border p-2 rounded-md"
     v-for="(image, index) in activeMarker?.photos"
     :key="index + 'img'"
     @click="{ activeImage = 'src/assets/img/test.jpg'; visibleModal = true }">
    <img class="object-cover rounded-sm w-full h-full mt-2  cursor-pointer hover:scale-101 transition duration-200"
         :src="image.file_url" />

</div>
<SlotModal v-if="activeImage && visibleModal"
           @close="visibleModal = false">
    <img class=" object-contain w-full h-full"
         :src="activeImage" />
</SlotModal>
</template>
<script lang="ts">
import { defineComponent, ref, type PropType } from 'vue';
import SlotModal from './layout/SlotModal.vue';
import type { IMapMarker } from '@/interfaces/IMapMarkers';

export default defineComponent({
    components: { SlotModal },
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