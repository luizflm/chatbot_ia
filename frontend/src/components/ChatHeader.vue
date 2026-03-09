<script setup>
import ChatIcon from './ChatIcon.vue';

defineProps({
    hasMessages: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['clear']);

const handleClear = () => {
    emit('clear');
}
</script>

<template>
    <header class="flex items-center justify-between px-6 py-4 border-b border-stone-200 bg-white shrink-0">
        <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-amber-50 border border-amber-200 flex items-center justify-center">
                <ChatIcon class="h-4 w-4" />
            </div>
            <span class="font-display font-bold text-lg tracking-tight text-stone-900">
                Chat<span class="text-amber-600">bot</span>
            </span>
        </div>

        <div class="flex items-center gap-3">
            <Transition
                enter-active-class="transition-all duration-200 ease-out"
                enter-from-class="opacity-0 translate-x-2"
                enter-to-class="opacity-100 translate-x-0"
                leave-active-class="transition-all duration-150 ease-in"
                leave-from-class="opacity-100 translate-x-0"
                leave-to-class="opacity-0 translate-x-2"
            >
                <button 
                    v-if="hasMessages" 
                    @click="handleClear"
                    class="flex items-center gap-1.5 text-xs text-stone-500 hover:text-stone-900 transition-all duration-200 px-3 py-1.5 rounded-lg hover:bg-stone-100 border border-transparent hover:border-stone-200"
                    title="Start a new conversation"
                >
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <path d="M12 5v14M5 12h14" />
                    </svg>
                    New chat
                </button>
            </Transition>
        </div>
    </header>
</template>