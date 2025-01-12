import { create } from 'zustand'

const useChat = create((set, get) => ({
  messages: [],
  isThinking: false,
  input: "",

  setInput: (input) => set(state => ({ ...state, input })),

  sendMessage: async () => {
    const userMessage = get().input.trim();
    if (!userMessage) return;

    // Show user message in UI
    set(state => ({
      ...state,
      input: "",
      isThinking: true,
      messages: [...state.messages, { text: userMessage, isUser: true }],
    }));

    try {
      // Start streaming response
      const response = await fetch('http://localhost:8080/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      // Stream partial text
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      // We'll add a "partial AI message" to track text as it arrives
      // or we can keep appending new messages, your choice
      let partialText = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) {
          set(state => ({ ...state, isThinking: false }));
          break;
        }
        // decode the chunk
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        for (let i=0; i < lines.length - 1; i++) {
          const line = lines[i].trim();
          if (line) {
            const parsed = JSON.parse(line);
            partialText = parsed.message;

            // Update messages with partialText
            // If you want a single message that keeps being updated, do this:
            set(state => {
              const lastMessage = state.messages[state.messages.length-1];
              if (lastMessage && !lastMessage.isUser) {
                // It's the partial AI msg
                lastMessage.text = partialText;
                return { ...state, messages: [...state.messages] }
              } else {
                // First chunk from AI -> push new AI msg
                return { 
                  ...state, 
                  messages: [...state.messages, { text: partialText, isUser: false }] 
                }
              }
            });
          }
        }
        // leftover partial
        buffer = lines[lines.length-1];
      }
    } catch (error) {
      console.error('Error:', error);
      set(state => ({
        ...state,
        isThinking: false,
        messages: [
          ...state.messages,
          { text: 'Sorry, an error occurred. Please try again.', isUser: false }
        ],
      }));
    }
  },
}));

export default useChat;
