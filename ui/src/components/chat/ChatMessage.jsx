import React from "react";
import Molecule from "@/assets/svg/molecule.svg";
import Markdown from "react-markdown";

// ChatMessage component for individual messages
const ChatMessage = ({ message, isUser }) => (
  <div>
    {isUser ? (
      <div className="border bg-card rounded-full w-fit px-4 py-4 grid grid-cols-[40px_1fr] items-center gap-x-4">
        <img
          className="rounded-full w-[40px] h-[40px]"
          src="/avatar.png"
          alt="avatar"
        />
        {message}
      </div>
    ) : (
      <div className="w-fit px-4 py-4 grid grid-cols-[40px_1fr] items-center gap-x-4">
        <div
          className="flex items-center justify-center w-[35px] h-[35px] rounded-xl"
          style={{
            background: "linear-gradient(180deg, #8F00FF 0%, #FE00E4 100%)",
          }}
        >
          <Molecule />
        </div>
        <div className="prose dark:prose-invert break-words">
          <Markdown>{message}</Markdown>
        </div>
      </div>
    )}
  </div>
);

export default ChatMessage;
