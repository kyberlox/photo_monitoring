<template>
<div class="fixed inset-0 flex items-center justify-center bg-[#00000052]"
     @click="$emit('close')">
    <div class="bg-white p-[12px] rounded-[8px] shadow-lg max-h-screen overflow-y-auto"
         @click.stop>
        <slot></slot>
    </div>
</div>
</template>