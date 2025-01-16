import React, { useRef, useEffect, useLayoutEffect } from "react";

import useChat from "./lib/store";
import { useShallow } from "zustand/react/shallow";
import ChatMessage from "./components/chat/ChatMessage";

import Thinking from "@/assets/svg/thinking.svg";
import Send from "@/assets/svg/send.svg";

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
    useLayoutEffect(() => {
        chatContainerRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' })
    }, [messages])

    return (
        <div className="relative min-h-screen min-w-screen bg-background">
            <main className="h-[calc(100svh-75px)] flex w-full flex-col px-2 overflow-scroll">

                <div ref={chatContainerRef} className="w-full lg:w-[800px] mx-auto py-12 rounded-2xl sm:mt-12 flex flex-col gap-y-4">
                    {messages.map((msg, index) => (
                        <ChatMessage key={index} message={msg.text} isUser={msg.isUser} />
                    ))}
                    {isThinking && (
                        <Thinking className="text-[#ea02e9] h-[30px] -mt-16 ml-9"/>
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
                        <Send/>
                    </button>
                </div>
            </footer>
        </div>
    );
}
