<script setup>
import { computed } from 'vue';
import AssistantAvatarIcon from './AssistantAvatarIcon.vue';
import ErrorAvatarIcon from './ErrorAvatarIcon.vue';

const props = defineProps({
    role: {
        type: String,
        required: true,
        validator: (value) => ['user', 'assistant', 'error'].includes(value),
    },
});

const isUser = computed(() => props.role === 'user');
const isAssistant = computed(() => props.role === 'assistant');
const isError = computed(() => props.role === 'error');

const avatarClass = computed(() => {
    if (isUser.value) return 'bg-amber-100 text-amber-700 border border-amber-200';
    if (isError.value) return 'bg-red-50 text-red-500 border border-red-200';
    return 'bg-stone-100 text-stone-500 border border-stone-200';
});
</script>

<template>
    <div class="shrink-0 mt-1">
        <div
            class="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold"
            :class="avatarClass"
        >
            <AssistantAvatarIcon v-if="isAssistant" />
            <ErrorAvatarIcon v-else-if="isError" />
            <span v-else>U</span>
        </div>
    </div>
</template>