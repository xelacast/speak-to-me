"use client";

import { type ChangeEvent, useState } from "react";

import { useMutation } from "@tanstack/react-query";
import LockBox, { type LockType } from "~/app/_components/lockbox";

export default function HomePage() {
  const [textInput, setTextInput] = useState("");
  const [lockState, setLockState] = useState<{
    color: string;
    lock_type: LockType;
  }>({
    color: "white",
    lock_type: "closed",
  });
  const [loading, setLoading] = useState(false);

  const onInput = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setTextInput(e.target.value);
  };

  const mutation = useMutation({
    mutationFn: (input: string) => {
      return fetch("http://localhost:8000/lock-assistant-v1/invoke", {
        method: "POST",
        body: JSON.stringify({ input: { input } }),
      });
    },
    onMutate: async (variables) => {
      console.log("on mutate", variables);
      setLoading(true);
    },
    onSuccess: async (data) => {
      setLoading(false);

      const { output } = (await data.json()) as {
        output: { color: string; message: string; lock_type: LockType };
      };
      console.log("Read Data: ", output);
      setLockState({ color: output.color, lock_type: output.lock_type });
    },
    onError: (error) => {
      console.log("Error: ", error);
    },
  });

  const onSend = () => {
    console.log("Sending to API then --> LLM --> client: ", textInput);
    const query = mutation.mutate(textInput);
    console.log("Query: ", query);
    setTextInput("");
  };
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-r from-cyan-500 to-blue-500">
      <h1 className="mb-4 text-4xl font-bold">
        Welcome to the LLM Emoji Color Changer
      </h1>
      <div className="flex gap-8">
        <div id="container-left" className="flex items-center">
          <LockBox color={lockState.color} lock_type={lockState.lock_type} />
        </div>
        <div id="container-right" className="flex flex-col gap-2 p-4">
          <label htmlFor="llm-text-entry">Talk to the LLM:</label>
          <textarea
            id="llm-text-entry"
            className="bg-gray opacity-4 h-[64px] w-[400px] rounded-lg p-3"
            onChange={(e) => onInput(e)}
            value={textInput ?? ""}
          />
          <div>{loading ? <span>Loading...</span> : <span></span>}</div>
          <button
            className="rounded-xl border border-slate-500 bg-slate-600 p-2 text-white opacity-95 transition-colors ease-in-out hover:bg-slate-700"
            onClick={onSend}
          >
            Send
          </button>
        </div>
      </div>
    </main>
  );
}
