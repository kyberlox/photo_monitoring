<template>
<div class="flex flex-col gap-4 w-full mt-4">
    <input class="rounded-md border border-gray-400 px-2 py-1 outline-none w-fit"
           v-model="name"
           placeholder="введите имя" />
    <div v-if="files.length"
         class="flex flex-col">
        добавленные файлы
        <div v-for="value in files">
            {{ value.name }}
        </div>
    </div>
    <div>
        Координаты: {{ coordinates }}
    </div>
    <div class="relative border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200 ease-in-out w-full min-h-[200px] "
         :class="{
            'border-blue-500 bg-blue-50': dragOver,
            'border-gray-300 bg-gray-50 hover:border-gray-400 hover:bg-gray-100': !dragOver,
        }"
         @dragover.prevent="dragOver = true"
         @dragleave.prevent="dragOver = false"
         @drop.prevent="handleDrop"
         @click="triggerFileInput">
        <input ref="fileInputRef"
               type="file"
               class="hidden"
               multiple
               @change="handleFileSelect" />
        <div class="flex flex-col items-center justify-center space-y-4 h-full">
            <div class="text-gray-700">
                <p class="text-lg font-medium">Перетащите файлы сюда</p>
                <p class="text-sm text-gray-500 mt-1">или нажмите для выбора</p>
            </div>
        </div>
    </div>
    <div class="flex w-auto border p-2 rounded-md bg-blue-50 hover:bg-blue-100 border-blue-500 cursor-pointer"
         @click="handleAddNewPoint">
        Добавить
    </div>
</div>
</template>
<script lang='ts'>
import { defineComponent, ref, type PropType } from 'vue';
import type { LngLat } from '@yandex/ymaps3-types';

export default defineComponent({
    components: {},
    emits: ['addNewPoint'],
    props: {
        coordinates: {
            type: Array,
            required: true
        }
    },
    setup(props, { emit }) {
        const fileInputRef = ref();
        const dragOver = ref(false);
        const files = ref<File[]>([]);
        const name = ref<string>('');
        const handleDrop = (e: DragEvent) => {
            if (e && e.dataTransfer) {
                const newFiles = Array.from(e.dataTransfer.files)
                files.value.push(...newFiles);
                dragOver.value = false
            }
        }

        const triggerFileInput = () => { (fileInputRef.value as HTMLInputElement).click() }

        const handleFileSelect = () => {
            const newFiles: File[] = Array.from((fileInputRef.value).files);
            files.value.push(...newFiles);
        }

        const handleAddNewPoint = () => {
            const newBody = new FormData();
            newBody.append('name', name.value);
            newBody.append('coord_y', String(props.coordinates[1]));
            newBody.append('coord_x', String(props.coordinates[0]));
            files.value.map(e => newBody.append('photos', e))
            emit('addNewPoint', newBody);
        }

        return {
            dragOver,
            fileInputRef,
            files,
            name,
            handleAddNewPoint,
            handleDrop,
            triggerFileInput,
            handleFileSelect,
        }
    }
});
</script>