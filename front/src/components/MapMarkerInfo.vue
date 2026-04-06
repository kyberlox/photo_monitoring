<template>
<div class="w-full h-full max-w-[650px] bg-gray-100 p-2">
    <div class="rounded-lg bg-white h-full w-full flex flex-col px-3">
        <div v-if="pageType == 'list'"
             class="flex flex-col items-start max-h-full overflow-y-auto">
            <MapMarkerInfoList :activeMarker="activeMarker"
                               :allPoints="allPoints"
                               @markerClicked="(id) => $emit('markerClicked', id)"
                               @deletePoint="(id) => $emit('deletePoint', id)" />
        </div>
        <div v-else-if="pageType == 'watch'"
             class="flex flex-col items-start  max-h-full overflow-y-auto">
            <MapMarkerInfoWatch :activeMarker="activeMarker"
                                @deletePhoto="(data) => $emit('deletePhoto', data)"
                                @updatePhoto="(data) => $emit('updatePhoto', data)" />
        </div>
        <div v-else-if="pageType == 'edit'"
             class="flex flex-col items-start gap-4 max-h-full ">
            <MapMarkerInfoEdit :coordinates="newCoordinates || []"
                               @coordinatesChange="(newCords) => $emit('coordinatesChange', newCords)"
                               @addNewPoint="(newData) => $emit('addNewPoint', newData)" />
        </div>
    </div>
</div>
</template>
<script lang='ts'>
import { defineComponent, ref, type PropType, computed } from 'vue';
import MapMarkerInfoWatch from './MapMarkerInfoWatch.vue';
import MapMarkerInfoList from './MapMarkerInfoList.vue';
import MapMarkerInfoEdit from './MapMarkerInfoEdit.vue';
import type { IMapMarker } from '@/interfaces/IMapMarkers';
import type { LngLat, YMapMarkerProps } from '@yandex/ymaps3-types';
export default defineComponent({
    components: { MapMarkerInfoWatch, MapMarkerInfoEdit, MapMarkerInfoList },
    emits: ['addNewPoint', 'changeActiveMarker', 'deletePoint', 'markerClicked', 'updatePhoto', 'deletePhoto', 'coordinatesChange'],
    props: {
        activeMarker: {
            type: Object as PropType<IMapMarker | null>
        },
        pageType: {
            type: String
        },
        newCoordinates: {
            type: Object as PropType<LngLat>
        },
        allPoints: {
            type: Array<IMapMarker>
        },
        updateKey: {
            type: Number,
        }
    },
    setup(props) {
        const updateKey = computed(() => props.updateKey);
        return {
            updateKey
        }
    }
});
</script>