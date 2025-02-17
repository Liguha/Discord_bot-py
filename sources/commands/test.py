import discord as ds
from ..core.storage import Item
from ..core.command import description, flag_group, storage_variable

@description("Test command (DEV).")
@flag_group(["flags", "content", "both"], "Which part of the command bot should print.",
            {
                "flags": "Bot should print only flags.",
                "content": "Bot should print only content.",
                "both": "Bot should print flags and content"
            })
@flag_group(["slave", "master"], "Undocumented flag group.")
@storage_variable("prefix")
def command(msg: ds.Message, flags: list[str | None], content: str, prefix: Item) -> list[str]:
    ans: str = ""
    if flags[0] != "content":
        ans += f"Flags: {flags}.\n"
    if flags[0] != "flags":
        ans += f"Content: {content}\n"
    ans += f"Prefix: {prefix.value}"
    return [ans]
