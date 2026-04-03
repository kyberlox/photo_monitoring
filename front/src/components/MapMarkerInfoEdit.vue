<template>
<div class="mt-5 w-full">
    <div v-if="!coordinates.length"
         class="text-lg mb-5">Укажите точку на карте</div>
    <div class="flex flex-col gap-4 w-full">
        <input class="rounded-md border border-gray-400 px-3 py-2 outline-none w-fit"
               v-model="name"
               placeholder="введите имя" />
        <div>
            Координаты: {{ coordinates }}
        </div>
        <FileLoader v-if="coordinates.length"
                    :coordinates="coordinates"
                    :name="name"
                    @addNewPoint="(newPoint) => $emit('addNewPoint', newPoint)" />
    </div>
</div>
</template>
<script lang='ts'>
import { defineComponent, ref, type PropType } from 'vue';
import type { LngLat } from '@yandex/ymaps3-types';
import FileLoader from './common/FileLoader.vue';

export default defineComponent({
    components: { FileLoader },
    emits: ['addNewPoint'],
    props: {
        coordinates: {
            type: Array,
            required: true
        }
    },
    setup(props, { emit }) {
        const name = ref();

        return {
            name
        }
    }
});
</script>