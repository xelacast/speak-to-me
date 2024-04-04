"use client";

import {
  LockClosedIcon,
  LockOpen1Icon,
  LockOpen2Icon,
} from "@radix-ui/react-icons";

export type LockType = "open" | "closed" | "half-opened";

interface Lock {
  color: string;
  lock_type: LockType;
}

export default function LockBox({ lock_type, color }: Lock) {
  // receive state of lockbox based on input of llm
  let lock: React.ReactNode;
  if (lock_type === "open") {
    lock = <LockOpen2Icon height={50} width={50} color={color} />;
  } else if (lock_type === "half-opened") {
    lock = <LockOpen1Icon height={50} width={50} color={color} />;
  } else {
    lock = <LockClosedIcon height={50} width={50} color={color} />;
  }

  return <div>{lock}</div>;
}
