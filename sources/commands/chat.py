import discord as ds
from openai import OpenAI
from ..core import Item, description, flag_group, storage_variable

@description("Chatbot LLM (DEV).")
@flag_group(["--reset"], "Flag to reset history")
@storage_variable("chatbot_client")
@storage_variable("chatbot_messages")
@storage_variable("externals")
async def command(msg: ds.Message, flags: list[str | None], content: str, 
                  chatbot_client: Item[OpenAI], chatbot_messages: Item[list], externals: Item[dict]) -> list[str]:
    if flags[0] == "--reset":
        extra: str = ""
        chatbot_messages.value = []
        if content != "":
            chatbot_messages.value.append({"role": "system", "content": content})
            extra = f" System prompt is '{content}'"
        return [f"Chat history refreshed.{extra}"]
    if chatbot_messages.value is None:
        chatbot_messages.value = []
    chatbot_messages.value.append({"role": "user", "content": content})
    client: OpenAI = chatbot_client.value
    answer: str | None = None
    while answer is None or answer == "":
        response = client.chat.completions.create(model=externals.value["chatbot_model"],
                                                  messages=chatbot_messages.value,
                                                  stream=False)
        answer = response.choices[0].message.content
    chatbot_messages.value.append({"role": "assistant", "content": answer})
    return [answer]