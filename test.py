import json
import os
from langchain_classic.memory import ConversationSummaryBufferMemory,ConversationSummaryMemory
from agents import llm
from langchain_core.messages import HumanMessage, AIMessage


## <------------ update chats ------------>
def append_to_chat(convname):
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
            
            print(len(data))
        
            print("making buffer memory")
            # If data length >= 20, use ConversationSummaryBufferMemory to summarize
        
        if len(data) > 0 and isinstance(data, list):
            print("making buffer memory")
            memory = ConversationSummaryMemory(
                llm=llm, max_token_limit=100, return_messages=True
            )
            # Add existing messages to memory
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
            buffer = memory.
            # Convert to dict format
            data = []
            for msg in buffer:
                if isinstance(msg, HumanMessage):
                    data.append(
                        {"role": "user", "content": msg.content, "ask_type": ""}
                    )
                elif isinstance(msg, AIMessage):
                    data.append({"role": "ai", "content": msg.content, "source": {}})

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

        return "chat updated"
        print(data)

    # except Exception as e:
    #     print(f"Error in append_to_chat: {e}")
    #     return str(e)
    
if __name__=="__main__":
    append_to_chat("Hello",)
