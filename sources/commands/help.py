import os
import discord as ds
from pathlib import Path
from ..core.bot import DiscordBot
from ..core.command import Command, description
from ..core.parser import CommandPareser


@description("Help notes")
def command(msg: ds.Message, flags: list[str], content: str) -> list[str]:
    if content == "":
        files = os.listdir(Path(__file__).parent)
        return ["; ".join(files)]
    parser: CommandPareser = CommandPareser(content)
    cmd: Command = parser.command
    flags: list[str] = parser.flags
    flag_desc: str = ""
    for i, flag in enumerate(flags):
        desc = cmd.flag_groups[i].flag_desc
        if flag is None or desc is None:
            fstr: str = str(cmd.flag_groups[i].flags).replace(",", " |").replace("'", "")
            flag_desc += f"\n{fstr}: {cmd.flag_groups[i].description}"
        else:
            flag_desc += f"\n{flag}: {desc[flag]}"
    return [f"{cmd.description}{flag_desc}"]