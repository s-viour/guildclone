import os
import sys
import logging
from discord.ext import commands
from guildclone import core, util

if __name__ == "__main__":
	log_level = os.environ.get('GUILDCLONE_LOGLEVEL', 'INFO').upper()
	logging.basicConfig(level=log_level)
	token = os.environ.get('GUILDCLONE_TOKEN')
	if not token:
		sys.exit('GUILDCLONE_TOKEN environment variable not found. quitting...')

	prefix = os.environ.get('GUILDCLONE_PREFIX') or ';'

	bot = commands.Bot(prefix)
	bot.add_cog(util.CommandErrorHandler(bot))
	bot.add_cog(core.Cog(bot))
	bot.run(token)