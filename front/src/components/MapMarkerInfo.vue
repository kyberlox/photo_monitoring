<template>
<div class="w-full h-full max-w-[650px] bg-gray-100 p-2">
    <div class="rounded-lg bg-white h-full w-full flex flex-col px-3">
        <div v-if="pageType == 'list'"
             class="flex flex-col items-start gap-4 max-h-full overflow-y-auto">
            <MapMarkerInfoList :activeMarker="activeMarker"
                               :allPoints="allPoints"
                               @markerClicked="(id) => $emit('markerClicked', id)"
                               @deletePoint="(id) => $emit('deletePoint', id)" />
        </div>
        <div v-else-if="pageType == 'watch'"
             class="flex flex-col items-start gap-4 max-h-full overflow-y-auto">
            <MapMarkerInfoWatch :activeMarker="activeMarker"
                                @updatePhoto="(data) => $emit('updatePhoto', data)" />
        </div>
        <div v-else-if="pageType == 'edit'"
             class="flex flex-col items-start gap-4 max-h-full ">
            <MapMarkerInfoEdit :coordinates="newCoordinates || []"
                               @addNewPoint="(newData) => $emit('addNewPoint', newData)" />
        </div>
    </div>
</div>
</template>
<script lang='ts'>
import { defineComponent, ref, type PropType } from 'vue';
import MapMarkerInfoWatch from './MapMarkerInfoWatch.vue';
import MapMarkerInfoList from './MapMarkerInfoList.vue';
import MapMarkerInfoEdit from './MapMarkerInfoEdit.vue';
import type { IMapMarker } from '@/interfaces/IMapMarkers';

export default defineComponent({
    components: { MapMarkerInfoWatch, MapMarkerInfoEdit, MapMarkerInfoList },
    emits: ['addNewPoint', 'changeActiveMarker', 'deletePoint', 'markerClicked', 'updatePhoto'],
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