<script setup>
import { ref, watch, nextTick } from 'vue'
import { useChat } from './composables/useChat.js'
import ChatHeader from './components/ChatHeader.vue'
import ChatMessage from './components/ChatMessage.vue'
import TypingIndicator from './components/TypingIndicator.vue'
import EmptyState from './components/EmptyState.vue'
import ChatInput from './components/ChatInput.vue'

const { messages, isLoading, sendMessage, clearMessages } = useChat();
const scrollContainer = ref(null);

watch(
  messages,
  async () => {
    await nextTick()
    const el = scrollContainer.value;
    if (el) el.scrollTop = el.scrollHeight;
  },
  { deep: true }
);
</script>

<template>
  <div class="flex flex-col h-screen bg-stone-50 overflow-hidden">
    <ChatHeader :hasMessages="messages.length > 0" @clear="clearMessages" />

    <main ref="scrollContainer" class="flex-1 overflow-y-auto px-4 py-6">
      <div class="max-w-2xl mx-auto w-full space-y-6">
        <EmptyState v-if="messages.length === 0" />

        <template v-else>
          <ChatMessage v-for="msg in messages" :key="msg.id" :message="msg" />
          <TypingIndicator v-if="isLoading" />
        </template>
      </div>
    </main>

    <div class="border-t border-stone-200 bg-white">
      <div class="max-w-2xl mx-auto w-full">
        <ChatInput :is-loading="isLoading" @send="sendMessage" />
      </div>
    </div>
  </div>
</template>
