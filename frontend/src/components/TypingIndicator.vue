<script setup>
import AssistantAvatarIcon from './AssistantAvatarIcon.vue';
import ChatDots from './ChatDots.vue';

</script>

<template>
    <div class="flex gap-3 animate-fade-up">
        <div class="shrink-0 mt-1">
            <div class="w-7 h-7 rounded-full bg-stone-100 border border-stone-200 flex items-center justify-center">
                <AssistantAvatarIcon class="text-stone-500" />
            </div>
        </div>

        <div class="flex items-center gap-1.5 px-4 py-3 rounded-2xl rounded-tl-sm bg-white border border-stone-200 shadow-sm shadow-stone-200">
            <ChatDots />
        </div>
    </div>
</template>