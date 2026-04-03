<template>
<VHeader @pageTypeChanged="pageTypeChanged"
         :pageType="pageType" />
<div class="flex flex-row w-full h-screen max-h-[calc(100vh-70px)]">
  <YandexMapFrame :allPoints=mapPoints
                  @markerClicked="markerClicked"
                  @mapClicked="mapClicked"
                  :pageType="pageType" />
  <MapMarkerInfo :activeMarker="activeMarker"
                 :allPoints=mapPoints
                 :newCoordinates="newCoordinates"
                 :pageType="pageType"
                 @markerClicked="markerClicked"
                 @deletePoint="deletePoint"
                 @addNewPoint="addNewPoint" />
</div>
</template>
<script lang='ts'>
import { defineComponent, onMounted, ref, computed } from 'vue';
import YandexMapFrame from './components/YandexMapFrame.vue';
import MapMarkerInfo from './components/MapMarkerInfo.vue';
import VHeader from './components/layout/VHeader.vue';
import Api from './utils/Api';
import { useMapInfoData } from './stores/mapInfo';
import type { YandexMapDefaultMarkerSettings } from 'vue-yandex-maps';
import type { LngLat, YMapMarkerProps } from '@yandex/ymaps3-types';
import type { IMapMarker } from './interfaces/IMapMarkers';

export default defineComponent({
  components: {
    YandexMapFrame,
    MapMarkerInfo,
    VHeader
  },
  props: {},
  setup() {
    const useMapInfo = useMapInfoData();
    const activePoint = ref();
    const activeMarker = ref<IMapMarker>();
    const pageType = ref('watch');
    const newCoordinates = ref<number[]>([]);

    const markerClicked = (newVal: IMapMarker) => {
      pageType.value = 'watch';
      activeMarker.value = newVal;
    }
    const pageTypeChanged = (type: string) => {
      pageType.value = type
    }
    const mapClicked = (e: YandexMapDefaultMarkerSettings) => {
      (newCoordinates.value as LngLat) = e.coordinates;
    }

    const getPoints = () => {
      Api.get('/locations/all')
        .then((data) => useMapInfo.setPoints(data))
    }

    const addNewPoint = (newData: IMapMarker) => {
      Api.post('/locations/add', newData)
        .then((data) => console.log(data))
        .finally(() => getPoints())
    }

    const deletePoint = (id: number) => {
      Api.delete(`/locations/id=${id}`)
        .then(data => console.log(data))
        .finally(() => getPoints())
    }

    onMounted(() => {
      getPoints();
    })

    return {
      activePoint,
      activeMarker,
      pageType,
      newCoordinates,
      addNewPoint,
      mapClicked,
      pageTypeChanged,
      markerClicked,
      getPoints,
      deletePoint,
      mapPoints: computed(() => useMapInfo.getPoints)
    }
  }
});
</script>