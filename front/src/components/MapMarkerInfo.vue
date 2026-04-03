<template>
<div class="w-full h-full max-w-[650px] bg-gray-100 p-2">
    <div class="rounded-lg bg-white h-full w-full flex flex-col px-3">
        <div v-if="(pageType == 'watch' ? !activeMarker : !newCoordinates?.length)">
            <div class="text-lg mt-5">Нажмите на точку на карте или выберите точку из списка</div>
            <div v-for="point in allPoints"
                 class="flex flex-row justify-between px-4"
                 :key="allPoints?.length">
                <div class="text-md text-blue-600 underline cursor-pointer hover:text-blue-400 duration-200"
                     @click="$emit('markerClicked', point)">
                    {{ point.name }}
                </div>
                <div class="text-sm text-red-600 underline cursor-pointer hover:text-red-400 duration-200"
                     @click="$emit('deletePoint', point.id)">
                    Удалить
                </div>
            </div>
        </div>
        <div v-if="activeMarker && pageType == 'watch'"
             class="flex flex-col items-start gap-4 max-h-full overflow-y-auto">
            <MapMarkerInfoWatch :activeMarker="activeMarker" />
        </div>
        <div v-if="newCoordinates?.length && pageType == 'edit'"
             class="flex flex-col items-start gap-4 max-h-full ">
            <MapMarkerInfoEdit :coordinates="newCoordinates"
                               @addNewPoint="(newData) => $emit('addNewPoint', newData)" />
        </div>
    </div>
</div>
</template>
<script lang='ts'>
import { defineComponent, ref, type PropType } from 'vue';
import MapMarkerInfoWatch from './MapMarkerInfoWatch.vue';
import MapMarkerInfoEdit from './MapMarkerInfoEdit.vue';
import type { IMapMarker } from '@/interfaces/IMapMarkers';

export default defineComponent({
    components: { MapMarkerInfoWatch, MapMarkerInfoEdit },
    emits: ['addNewPoint', 'changeActiveMarker', 'deletePoint', 'markerClicked'],
    props: {
        activeMarker: {
            type: Object as PropType<IMapMarker>
        },
        pageType: {
            type: String
        },
        newCoordinates: {
            type: Array<number>
        },
        allPoints: {
            type: Array<IMapMarker>
        }
    },
});
</script>