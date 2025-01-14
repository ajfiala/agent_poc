import React, { useRef, useEffect } from "react";
import useChat from "./lib/store";
import { useShallow } from "zustand/react/shallow";
import ChatMessage from "./components/chat/ChatMessage";

// Main App component
export default function App() {
  const [input, setInput, messages, sendMessage, isThinking] = useChat(
    useShallow((state) => [
      state.input,
      state.setInput,
      state.messages,
      state.sendMessage,
      state.isThinking,
    ])
  );

  const chatContainerRef = useRef(null);

  // Scroll to bottom of chat when new messages are added
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="relative min-h-screen min-w-screen bg-background">
      <main className="flex w-full flex-col px-2">
        <div
          ref={chatContainerRef}
          className="w-full lg:w-[800px] mx-auto py-12 rounded-2xl sm:mt-12 flex flex-col gap-y-4"
        >
          {messages.map((msg, index) => (
            <ChatMessage key={index} message={msg.text} isUser={msg.isUser} />
          ))}
          {isThinking && (
            <div style={{ textAlign: "center", color: "#000000" }}>
              <p>Loading...</p>
            </div>
          )}
        </div>
      </main>
      <footer className="fixed bottom-0 left-0 w-full flex items-center justify-center p-6">
        <div className="relative flex items-center w-full lg:w-[800px] h-[60px] rounded-2xl border">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Type your message..."
            className="w-full h-full bg-input px-4 rounded-2xl"
          />
          <button
            onClick={sendMessage}
            disabled={isThinking}
            className="text-primary absolute bottom-0 right-4 h-full hover:scale-110 transition-transform"
          >
            <svg
              width="30"
              height="30"
              viewBox="0 0 30 30"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fillRule="evenodd"
                clipRule="evenodd"
                d="M12.6892 15.8963L8.19193 14.3972C5.83872 13.6128 4.66211 13.2206 4.66211 12.4999C4.66211 11.7791 5.83872 11.3869 8.19193 10.6025L21.2051 6.26476C22.8609 5.71283 23.6888 5.43687 24.1258 5.87388C24.5628 6.3109 24.2869 7.1388 23.7349 8.79459L19.3972 21.8078L19.3972 21.8078C18.6128 24.161 18.2206 25.3376 17.4998 25.3376C16.7791 25.3376 16.3869 24.161 15.6025 21.8078L14.1034 17.3105L19.4569 11.957C19.8475 11.5664 19.8475 10.9333 19.4569 10.5427C19.0664 10.1522 18.4332 10.1522 18.0427 10.5427L12.6892 15.8963Z"
                fill="currentColor"
              />
            </svg>
          </button>
        </div>
      </footer>
    </div>
  );
}
