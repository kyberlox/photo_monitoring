<template>
<YandexMap v-model="map"
           :settings="{
            location: {
                zoom: 9,
                center: [46.852501, 52.020287]
            },
        }"
           width="100%"
           height="100%">
    <YandexMapDefaultSchemeLayer />
    <YandexMapDefaultFeaturesLayer />
    <YandexMapDefaultMarker v-if="allPoints?.length"
                            v-for="point in allPoints"
                            :id=point.id
                            :settings="{ coordinates: point.coordinates as LngLat, onClick: () => $emit('markerClicked', point) }">
    </YandexMapDefaultMarker>
    <YandexMapDefaultMarker v-if="newPoint && newPoint.coordinates?.length"
                            :id=newPoint.id
                            :settings="{ coordinates: newPoint.coordinates }">
    </YandexMapDefaultMarker>
    <YandexMapListener v-if="pageType == 'edit'"
                       :settings="{ onClick: onMapClick }" />
</YandexMap>
</template>
<script lang='ts'>
import { defineComponent, ref, watch } from 'vue';
import { shallowRef } from 'vue';
import type { LngLat, YMap } from '@yandex/ymaps3-types';
import {
    YandexMap,
    YandexMapDefaultSchemeLayer,
    YandexMapDefaultFeaturesLayer,
    YandexMapDefaultMarker,
    YandexMapListener,
} from 'vue-yandex-maps';
import type { DomEventHandler } from '@yandex/ymaps3-types';
import type { IMapMarker } from '@/interfaces/IMapMarkers';

export default defineComponent({
    components: {
        YandexMap, YandexMapDefaultMarker, YandexMapDefaultSchemeLayer,
        YandexMapDefaultFeaturesLayer,
        YandexMapListener,
    },
    props: {
        pageType: {
            type: String
        },
        allPoints: {
            type: Array<IMapMarker>
        }
    },
    emits: ['markerClicked', 'mapClicked'],
    setup(props, { emit }) {
        const map = shallowRef<null | YMap>(null);
        const newPoint = ref<IMapMarker>({ coordinates: null });

        watch((props), () => {
            if (props.pageType)
                newPoint.value = ({ coordinates: null });
        }, { deep: true })

        const onMapClick: DomEventHandler = (object, event) => {
            newPoint.value.coordinates = event.coordinates;
            emit('mapClicked', event)
        };

        return { map, onMapClick, newPoint }
    }
});
</script>