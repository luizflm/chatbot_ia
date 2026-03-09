<script setup>
import { computed } from 'vue';
import MessageAvatar from './MessageAvatar.vue';
import FileBadge from './FileBadge.vue';

const props = defineProps({
    message: {
        type: Object,
        required: true,
    },
});

const isUser = computed(() => props.message.role === 'user');
const isError = computed(() => props.message.role === 'error');

const bubbleClass = computed(() => {
    if (isUser.value) return 'bg-amber-500 text-white rounded-tr-sm shadow-sm shadow-amber-200';
    if (isError.value) return 'bg-red-50 text-red-700 border border-red-200';
    return 'bg-white text-stone-900 border border-stone-200 rounded-tl-sm shadow-sm shadow-stone-200';
});
</script>

<template>
    <div class="flex gap-3 animate-fade-up" :class="isUser ? 'flex-row-reverse' : 'flex-row'">
        <MessageAvatar :role="message.role" />

        <div class="flex flex-col gap-1.5 max-w-[75%]" :class="isUser ? 'items-end' : 'items-start'">
            <FileBadge v-if="message.file" :file="message.file" />

            <div class="px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap" :class="bubbleClass">
                {{ message.content }}
            </div>
        </div>
    </div>
</template>
