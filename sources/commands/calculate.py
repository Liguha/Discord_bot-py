import discord as ds
from ..core.bot import DiscordBot
from ..core.command import description, flag_group

@description("Python eval")
def command(bot: DiscordBot, msg: ds.Message, flags: list[str], content: str) -> list[str]:
    ans = str(eval(content))
    return [ans]