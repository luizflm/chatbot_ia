<script setup>
import { ref, computed, nextTick } from 'vue';
import FileUploadBadge from './FileUploadBadge.vue';

const props = defineProps({
    isLoading: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['send']);

const inputText = ref('');
const attachedFile = ref(null);
const isFocused = ref(false);
const fileInput = ref(null);
const textareaRef = ref(null);
const canSubmit = computed(() => inputText.value.trim().length > 0 && !props.isLoading);

const triggerFileInput = () => fileInput.value?.click();

const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') attachedFile.value = file;
    event.target.value = '';
}

const removeFile = () => attachedFile.value = null;


const submit = async () => {
    if (!canSubmit.value) return;
    emit('send', inputText.value, attachedFile.value);
    inputText.value = '';
    attachedFile.value = null;
    await nextTick();
    if (textareaRef.value) textareaRef.value.style.height = 'auto';
};

const autoResize = () => {
    const el = textareaRef.value;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = el.scrollHeight + 'px';
}
</script>

<template>
    <div class="px-4 pb-5 pt-3 shrink-0">
        <div v-if="attachedFile" class="mb-2 pl-1">
            <FileUploadBadge :file="attachedFile" @remove="removeFile" />
        </div>

        <div class="flex items-end gap-2 bg-white border rounded-2xl px-5 py-2.5 transition-all duration-200"
            :class="isFocused ? 'border-amber-400 shadow-md shadow-amber-100' : 'border-stone-200 shadow-sm shadow-stone-100'"
        >
            <div>
                <button 
                    @click="triggerFileInput" 
                    :disabled="isLoading"
                    class="shrink-0 mb-0.5 w-8 h-8 flex items-center justify-center rounded-lg text-stone-400 hover:text-amber-600 hover:bg-amber-50 transition-all duration-200 disabled:opacity-30 disabled:cursor-not-allowed"
                    title="Attach a PDF"
                >
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path
                            d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
                    </svg>
                </button>

                <input 
                    ref="fileInput" 
                    type="file" 
                    accept="application/pdf" 
                    class="hidden" 
                    @change="handleFileSelect" 
                />
            </div>

            <div class="flex flex-1 self-center">
                <textarea 
                    ref="textareaRef" 
                    v-model="inputText" 
                    @keydown.enter.exact.prevent="submit"
                    @focus="isFocused = true" 
                    @blur="isFocused = false" 
                    @input="autoResize" 
                    :disabled="isLoading"
                    placeholder="Ask me anything..." 
                    rows="1"
                    class="flex-1 bg-transparent text-stone-900 placeholder-stone-500 resize-none outline-none leading-relaxed max-h-36 overflow-y-auto scrollbar-hide disabled:opacity-50" />
            </div>
            
            <div>
                <button 
                    @click="submit" 
                    :disabled="!canSubmit"
                    class="shrink-0 mb-0.5 w-8 h-8 flex items-center justify-center rounded-lg transition-all duration-200"
                    :class="canSubmit ? 
                        'bg-amber-500 text-white hover:bg-amber-600 shadow-md shadow-amber-200' : 
                        'bg-stone-100 text-stone-300 cursor-not-allowed'"
                >
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <line x1="22" y1="2" x2="11" y2="13" />
                        <polygon points="22 2 15 22 11 13 2 9 22 2" />
                    </svg>
                </button>
            </div>

        </div>

        <p class="text-center text-xs text-stone-300 mt-2">
            Enter to send &nbsp;·&nbsp; Shift+Enter for new line
        </p>
    </div>
</template>
