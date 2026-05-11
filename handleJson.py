import json
import os


## <------------ update chats ------------>
def append_to_chat(convname, new_entry):

    try:
        chatAddr = f"chats/{convname}"
        chatFile = f"{chatAddr}/chat.json"
 
        if not os.path.isdir(chatAddr):
            print("creating")
            os.makedirs(chatAddr)
            initial_data = {"chat": [{}]}
            with open(chatFile, "w") as f:
                json.dump(initial_data, f, indent=4)

        with open(chatFile, "r") as f:
            data = json.load(f)

        chat_obj = data["chat"][0]

        next_num = str(max(int(k) for k in chat_obj.keys()) + 1) if chat_obj else "0"
        chat_obj[next_num] = new_entry

        with open(chatFile, "w") as f:
            json.dump(data, f, indent=4)

        print("chat updated")
        return "success"

    except Exception as e:
        print(f"Error in append_to_chat: {e}")
        return str(e)
