"use client";

import { type ChangeEvent, useState } from "react";

export default function LLMChatBox() {
  const [textInput, setTextInput] = useState("");

  const onInput = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setTextInput(e.target.value);
  };

  const onSend = () => {
    // send to the api? Or LLM?
    console.log("Sending to LLM: ", textInput);
    setTextInput("");
  };

  return (
    <div id="container-right" className="flex flex-col gap-2 p-4">
      <label htmlFor="llm-text-entry">Talk to the LLM:</label>
      <textarea
        id="llm-text-entry"
        className="bg-gray opacity-4 h-[64px] w-[400px] rounded-lg p-3"
        onChange={(e) => onInput(e)}
        value={textInput ?? ""}
      />
      <button
        className="rounded-xl border border-slate-500 bg-slate-600 p-2 text-white opacity-95 transition-colors ease-in-out hover:bg-slate-700"
        onClick={onSend}
      >
        Send
      </button>
    </div>
  );
}
