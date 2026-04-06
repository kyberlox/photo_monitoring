<template>
<div class="relative mt-4 w-full border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200 ease-in-out w-full min-h-[200px] "
     :class="{
        'border-blue-500 bg-blue-50': dragOver,
        'border-gray-300 bg-gray-50 hover:border-gray-400 hover:bg-gray-100': !dragOver,
    }"
     @dragover.prevent="dragOver = true"
     @dragleave.prevent="dragOver = false"
     @drop.prevent="handleDrop"
     @click="triggerFileInput">
    <input :ref="'fileInputRef'"
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
<div class="flex w-fit border p-2 rounded-md bg-blue-50 hover:bg-blue-100 border-blue-500 cursor-pointer mt-2"
     @click="handleAddNewPoint">
    Добавить
</div>
<div v-if="files.length"
     class="flex flex-col">
    добавленные файлы
    <div v-for="value in files">
        {{ value.name }}
    </div>
</div>
</template>
<script lang='ts'>
import { defineComponent, ref } from 'vue';

export default defineComponent({
    components: {},
    emits: ['addNewPoint'],
    props: {
        coordinates: {
            type: Array,
            required: true
        },
        name: {
            type: String
        }
    },
    setup(props, { emit }) {
        const fileInputRef = ref();
        const dragOver = ref(false);
        const files = ref<File[]>([]);

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
            newBody.append('name', props.name || '');
            newBody.append('coord_y', String(props.coordinates[1]));
            newBody.append('coord_x', String(props.coordinates[0]));
            files.value.map(e => newBody.append('photos', e))
            emit('addNewPoint', newBody);
        }
        return {
            dragOver,
            handleDrop,
            triggerFileInput,
            handleFileSelect,
            handleAddNewPoint,
            files,
            fileInputRef
        }
    }
});
</script>