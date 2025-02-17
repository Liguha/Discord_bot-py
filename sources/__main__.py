from .core import DiscordBot
import os
import sys
sys.path.append(os.path.realpath('.'))

bot = DiscordBot()
bot.run()