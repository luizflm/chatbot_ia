<script setup>
import ChatIcon from './ChatIcon.vue';
</script>

<template>
    <div class="flex flex-col items-center justify-center h-full gap-8 px-6 py-16 animate-fade-up">
        <div class="relative">
            <div class="w-16 h-16 rounded-2xl bg-amber-50 border border-amber-200 flex items-center justify-center">
                <ChatIcon class="w-7 h-7" stroke-width="1.5" />
            </div>
            <div
                class="absolute -bottom-1 -right-1 w-5 h-5 rounded-full bg-emerald-50 border border-emerald-300 flex items-center justify-center">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            </div>
        </div>
        
        <div class="text-center">
            <h1 class="font-display font-bold text-2xl text-stone-900 mb-2">How can I help?</h1>
            <p class="text-sm text-stone-500 max-w-xs leading-relaxed">
                Ask me anything. Attach a PDF and I will answer based on its contents.
            </p>
        </div>
    </div>
</template>
