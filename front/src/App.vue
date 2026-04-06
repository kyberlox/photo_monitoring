<template>
<VHeader @pageTypeChanged="pageTypeChanged"
         :pageType="pageType" />
<div class="flex flex-row w-full h-screen max-h-[calc(100vh-70px)]">
  <YandexMapFrame :allPoints=mapPoints
                  @markerClicked="markerClicked"
                  @mapClicked="mapClicked"
                  :newCoordinates="newCoordinates"
                  :pageType="pageType" />
  <MapMarkerInfo :activeMarker="activeMarker"
                 :allPoints=mapPoints
                 :newCoordinates="newCoordinates"
                 :pageType="pageType"
                 :updateKey="updateKey"
                 @coordinatesChange="(newCords) => newCoordinates = newCords"
                 @markerClicked="markerClicked"
                 @deletePoint="deletePoint"
                 @addNewPoint="addNewPoint"
                 @updatePhoto="updatePhoto"
                 @deletePhoto="deletePhoto" />
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
    const activeMarker = ref<IMapMarker | null>();
    const pageType = ref('watch');
    const newCoordinates = ref<number[]>([]);
    const updateKey = ref(0);

    const markerClicked = (newVal: IMapMarker) => {
      pageType.value = 'watch';
      activeMarker.value = newVal;
    }
    const pageTypeChanged = (type: string) => {
      pageType.value = type;
      if (type !== 'watch') {
        activeMarker.value = {};
      }
      newCoordinates.value = [];
    }
    const mapClicked = (e: YandexMapDefaultMarkerSettings) => {
      (newCoordinates.value as LngLat) = e.coordinates;
    }

    const getPoints = () => {
      Api.get('/locations/all')
        .then((data) => useMapInfo.setPoints(data))
        .finally(() => {
          if (activeMarker.value) {
            if (activeMarker.value && 'id' in activeMarker.value)
              activeMarker.value = useMapInfo.getPoints.find(e => e.id == activeMarker.value?.id)
          }
        })
    }

    const addNewPoint = (newData: IMapMarker) => {
      Api.post('/locations/add', newData)
        .then((data) => { pageType.value = 'watch'; activeMarker.value = data; })
        .finally(() => getPoints())

    }

    const deletePoint = (id: number) => {
      Api.delete(`/locations/id=${id}`)
        .finally(() => getPoints())
    }

    const updatePhoto = (data: FormData) => {
      if (!activeMarker.value?.id) return
      const id = activeMarker.value.id;
      const updateBody = new FormData();
      const updatedPhotos = data.getAll('photos');
      updateBody.append('location_id', String(id));
      updatedPhotos.forEach(e => updateBody.append('photos', e))
      Api.post(`photos/add`, updateBody)
        .then(() => getPoints())
    }

    const deletePhoto = (id: number) => {
      Api.delete(`photos/id=${id}`)
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
      updateKey,
      addNewPoint,
      mapClicked,
      pageTypeChanged,
      markerClicked,
      getPoints,
      deletePoint,
      updatePhoto,
      deletePhoto,
      mapPoints: computed(() => useMapInfo.getPoints)
    }
  }
});
</script>