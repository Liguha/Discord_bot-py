import discord as ds
from ..core import description, flag_group

@description("Python eval")
async def command(msg: ds.Message, flags: list[str], content: str) -> list[str]:
    ans = str(eval(content))
    return [ans]