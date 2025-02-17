import discord as ds
from ..core.bot import DiscordBot
from ..core.command import description, flag_group

@description("Test command (DEV).")
@flag_group(["flags", "content", "both"], "Which part of the command bot should print.",
            {
                "flags": "Bot should print only flags.",
                "content": "Bot should print only content.",
                "both": "Bot should print flags and content"
            })
@flag_group(["slave", "master"], "Undocumented flag group.")
def command(bot: DiscordBot, msg: ds.Message, flags: list[str], content: str) -> list[str]:
    ans: str = ""
    if flags[0] != "content":
        ans += f"Flags: {flags}.\n"
    if flags[0] != "flags":
        ans += f"Content: {content}\n"
    return [ans]
