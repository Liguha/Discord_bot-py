import discord as ds
from openai import OpenAI
from ..core.storage import Item
from ..core.command import description, flag_group, storage_variable

@description("DeepSeek v3 LLM (DEV).")
@flag_group(["reset"])
@storage_variable("deepseek_client")
@storage_variable("deepseek_messages")
async def command(msg: ds.Message, flags: list[str | None], content: str, 
                  deepseek_client: Item, deepseek_messages: Item) -> list[str]:
    if flags[0] == "reset":
        extra: str = ""
        deepseek_messages.value = []
        if content != "":
            deepseek_messages.value.append({"role": "system", "content": content})
            extra = f" System prompt is '{content}'"
        return [f"Chat history refreshed.{extra}"]
    if deepseek_messages.value is None:
        deepseek_messages.value = []
    deepseek_messages.value.append({"role": "user", "content": content})
    client: OpenAI = deepseek_client.value
    answer: str | None = None
    while answer is None or answer == "":
        response = client.chat.completions.create(model="deepseek/deepseek-chat:free",
                                                  messages=deepseek_messages.value,
                                                  stream=False)
        answer = response.choices[0].message.content
        print(answer, len(response.choices))
    deepseek_messages.value.append({"role": "assistant", "content": answer})
    return [answer]