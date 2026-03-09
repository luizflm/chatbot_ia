import { ref, readonly } from 'vue';

const API_URL = 'http://localhost:8000/query';

export function useChat() {
    const messages = ref([]);
    const isLoading = ref(false);
    const error = ref(null);

    const sendMessage = async (text, file = null) => {
        if (!text.trim() || isLoading.value) return;

        error.value = null;

        messages.value.push({
            id: Date.now(),
            role: 'user',
            content: text.trim(),
            file: file ? { name: file.name } : null,
        });

        isLoading.value = true;

        try {
            const formData = new FormData();
            formData.append('message', text.trim());

            if (file) {
                formData.append('file', file);
            }

            const response = await fetch(API_URL, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(errData.detail || `Server error: ${response.status}`);
            }

            const data = await response.json();

            messages.value.push({
                id: Date.now() + 1,
                role: 'assistant',
                content: data.answer,
            });
        } catch (err) {
            error.value = err.message || 'An unexpected error occurred.';
            messages.value.push({
                id: Date.now() + 2,
                role: 'error',
                content: error.value,
            });
        } finally {
            isLoading.value = false;
        }
    };

    const clearMessages = () => {
        messages.value = [];
        error.value = null;
    };

    return {
        messages: readonly(messages),
        isLoading: readonly(isLoading),
        error: readonly(error),
        sendMessage,
        clearMessages,
    };
}