<template>
<div class="flex flex-row flex-wrap py-[2px] px-[32px] justify-between items-center ">
    <div class="py-[9px]">
        <LogoIcon />
    </div>
    <div class="flex flex-row gap-4">
        <div v-for="(type, index) in pageTypes"
             :key="'hroute' + index"
             class="cursor-pointer hover:text-orange-400 duration-200"
             :class="{ 'underline text-orange-600': pageType == type.name }"
             @click="$emit('pageTypeChanged', type.name)">
            {{ type.title }}
        </div>
    </div>
</div>
</template>
<script lang='ts'>
import { defineComponent } from 'vue';
import LogoIcon from '@/assets/img/logo.svg?component';

export default defineComponent({
    components: {
        LogoIcon
    },
    props: {
        pageType: {
            type: String
        }
    },
    setup() {
        return {
            pageTypes: [{ title: 'Все точки', 'name': 'list' }, { title: 'Просмотр', name: 'watch' }, { title: 'Добавить точку', 'name': 'edit' }]
        }
    }
});
</script>