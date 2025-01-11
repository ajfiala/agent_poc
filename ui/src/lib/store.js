import { create } from 'zustand'

const useChat = create((set, get) => ({
    messages: [],
    isThinking: false,
    input: "",
    setInput: (input) => set(state => ({ ...state, input })),

    sendMessage: async () => {
        if (!get().input.trim()) return;

        const userMessage = get().input.trim();
        set(state => ({ 
            ...state, 
            input: '',
            isThinking: true,
            messages: [...state.messages, { text: userMessage, isUser: true }],
        }))

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            set(state => ({ 
                ...state,
                messages: [...state.messages, { text: data.response, isUser: false }],
            }))

        } catch (error) {
            console.error('Error:', error);
            set(state => ({ 
                ...state,
                messages: [
                    ...state.messages, 
                    { text: 'Sorry, an error occurred. Please try again.', isUser: false }
                ],
            }))

        } finally {
            set(state => ({ ...state, isThinking: false, }))
        }
    },

}))

export default useChat;