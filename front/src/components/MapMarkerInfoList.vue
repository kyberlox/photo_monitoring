<template>
<div class="text-lg mt-5">Выберите точку из списка</div>
<div v-for="point in allPoints"
     :key="point.id"
     class="flex flex-row justify-between px-4 w-full">
    <div class="text-md text-blue-600 underline cursor-pointer hover:text-blue-400 duration-200"
         @click="$emit('markerClicked', point)">
        {{ point.name }}
    </div>
    <div class="text-sm text-red-600 underline cursor-pointer hover:text-red-400 duration-200"
         @click="$emit('deletePoint', point.id)">
        Удалить
    </div>
</div>
</template>
<script lang='ts'>
import { defineComponent, type PropType } from 'vue';
import type { IMapMarker } from '@/interfaces/IMapMarkers';

export default defineComponent({
    components: {},
    emits: ['deletePoint', 'markerClicked'],

    props: {
        activeMarker: {
            type: Object as PropType<IMapMarker>
        },
        pageType: {
            type: String
        },
        allPoints: {
            type: Array<IMapMarker>
        }
    },
    setup() {
        return {}
    }
});
</script>