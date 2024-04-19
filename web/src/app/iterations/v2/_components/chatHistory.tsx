import clsx from "clsx";

export const ChatHistory = ({
  history,
}: {
  history: { type: "ai" | "human"; message: string }[] | [];
}) => {
  return (
    <div className="overflow h-[60vh] w-[60vw] rounded-lg bg-slate-200 bg-opacity-40 p-4">
      <ul className="flex flex-col gap-4">
        {history.map((mes, i) => {
          const message_type = mes.type === "human";
          return (
            <li
              key={i}
              className={clsx(
                message_type ? "self-end" : "self-start",
                "rounded-lg bg-gray-950 bg-opacity-35 p-2",
              )}
            >
              <p className="text-white">
                {mes.type} - {mes.message}
              </p>
            </li>
          );
        })}
      </ul>
    </div>
  );
};
