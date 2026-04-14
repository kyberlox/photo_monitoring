<template>
<div class="mt-5 w-full">
    <div v-if="!coordinates.length"
         class="text-lg mb-5">Укажите точку на карте</div>
    <div class="flex flex-col w-full">
        <input class="rounded-md border border-gray-400 px-3 py-2 outline-none w-fit"
               v-model="name"
               placeholder="введите имя" />
        <span class="mt-2">Координаты:</span>
        <input class="rounded-md border border-gray-400 px-3 py-2 outline-none w-full mt-1"
               v-model="inputCoordinates"
               @change="$emit('coordinatesChange', inputCoordinates ? String(inputCoordinates).split(',').map((e) => Number(e)) : [])"
               placeholder="введите координаты" />
        <FileLoader v-if="coordinates.length"
                    :coordinates="coordinates"
                    :name="name"
                    @addNewPoint="(newPoint) => $emit('addNewPoint', newPoint)" />
    </div>
</div>
</template>
<script lang='ts'>
import { defineComponent, ref, watch, type PropType, computed } from 'vue';
import type { LngLat } from '@yandex/ymaps3-types';
import FileLoader from './common/FileLoader.vue';

export default defineComponent({
    components: { FileLoader },
    emits: ['addNewPoint', 'coordinatesChange'],
    props: {
        coordinates: {
            type: Object as PropType<LngLat | []>,
            required: true
        }
    },
    setup(props) {
        const name = ref();
        const inputCoordinates = ref();
        watch(props, () => {
            if (props.coordinates.length > 1)
                inputCoordinates.value = String(props.coordinates).split(',').map((e) => Number(e));
        }, { immediate: true, deep: true })

        return {
            name,
            inputCoordinates
        }
    }
});
</script>