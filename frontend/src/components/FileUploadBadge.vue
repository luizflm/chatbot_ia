<script setup>
import { computed } from 'vue';

const props = defineProps({
    file: {
        type: File,
        required: true
    },
});

defineEmits(['remove']);

const fileName = computed(() => props.file.name);

const fileSize = computed(() => {
    const bytes = props.file.size;
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
});
</script>

<template>
    <div class="flex items-center gap-2 px-3 py-2 bg-amber-50 border border-amber-200 rounded-xl">
        <svg class="w-4 h-4 text-amber-600 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor"
            stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="16" y1="13" x2="8" y2="13" />
            <line x1="16" y1="17" x2="8" y2="17" />
            <polyline points="10 9 9 9 8 9" />
        </svg>

        <span class="text-xs text-amber-800 truncate max-w-45">{{ fileName }}</span>

        <span class="text-xs text-stone-400 shrink-0">{{ fileSize }}</span>

        <button @click="$emit('remove')"
            class="ml-1 shrink-0 text-stone-400 hover:text-red-500 transition-colors duration-150" title="Remove file">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
        </button>
    </div>
</template>