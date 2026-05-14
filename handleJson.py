import json
import os
from langchain_classic.memory import ConversationSummaryMemory
from agents import llm


## <------------ update chats ------------>
def append_to_chat(convname, new_entry):
    """
    new_entry format:
    {
        "human": "user query",
        "ai": "ai response",
        "queryType": "ask/deep_research/deep_thinking",
        "source": {...}
    }
    """
    try:
        chatAddr = f"chats/{convname}"
        chatFile = f"{chatAddr}/chat.json"

        if not os.path.isdir(chatAddr):
            print("creating new folder")
            os.makedirs(chatAddr)
            initial_data = []
            with open(chatFile, "w") as f:
                json.dump(initial_data, f, indent=4)

        with open(chatFile, "r") as f:
            data = json.load(f)

        # Ensure data is a list
        if not isinstance(data, list):
            data = []

        # If data length >= 30, use ConversationSummaryBufferMemory to summarize
        if len(data) >= 30:
            memory = ConversationSummaryMemory(
                llm=llm, max_token_limit=3000, return_messages=True
            )

            # Check if previous summary exists and add it first
            if data and data[0].get("role") == "previousChatSummerized":
                previous_summary = data[0]["content"]
                memory.save_context(
                    {"input": f"Previous conversation context: {previous_summary}"},
                    {"output": "Continuing from previous context."},
                )

            # Then add all the user/ai pairs
            for i in range(0, len(data), 2):
                if (
                    i + 1 < len(data)
                    and data[i].get("role") == "user"
                    and data[i + 1].get("role") == "ai"
                ):
                    memory.save_context(
                        {"input": data[i]["content"]},
                        {"output": data[i + 1]["content"]},
                    )
                    # Get the buffer
            buffer = memory.buffer
            # Convert to dict format
            data = []
            data.append({"role": "previousChatSummerized", "content": buffer})

        # Append user message
        data.append(
            {
                "role": "user",
                "content": new_entry.get("human", ""),
                "ask_type": new_entry.get("queryType", ""),
            }
        )

        # Append AI message
        data.append(
            {
                "role": "ai",
                "content": new_entry.get("ai", ""),
                "source": new_entry.get("source", ""),
            }
        )

        with open(chatFile, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return f"chat updated for {convname}"

    except Exception as e:
        return f"Error in append_to_chat: {e}"
