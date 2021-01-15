import os
import sys
import logging
from discord.ext import commands
import core
import util


if __name__ == "__main__":
	log_level = os.environ.get('BOT_LOGLEVEL', 'INFO').upper()
	logging.basicConfig(level=log_level)
	token = os.environ.get('BOT_TOKEN')
	if not token:
		sys.exit('BOT_TOKEN environment variable not found. quitting...')

	prefix = os.environ.get('BOT_PREFIX') or ';'

	bot = commands.Bot(prefix)
	bot.add_cog(util.CommandErrorHandler(bot))
	bot.add_cog(core.Cog(bot))
	bot.run(token)