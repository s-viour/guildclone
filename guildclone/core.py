import logging
import discord
from discord.ext import commands
from .util import GuildMapping


logger = logging.getLogger('guildclone')


async def clone_server_roles(dstguild, srcguild):
	"""clones the roles of srcguild into dstguild.
	returns a mapping of the source guild's roles to
	the corresponding role in the destination server,
	this mapping is for supplying to clone_server_channels
	to get the overwrites correct
	"""
	mapping = {}

	for role in srcguild.roles:
		if not role.is_default() and not role.managed:
			logger.info(f'creating role {role}')
			nrole = await dstguild.create_role(
				name=role.name,
				permissions=role.permissions,
				colour=role.colour,
				hoist=role.hoist,
				mentionable=role.mentionable,
				reason=f'cloning guild from {srcguild.id}'
			)

			mapping[role] = nrole

	mapping[srcguild.default_role] = dstguild.default_role

	return mapping

def convert_overwrites(overwrites, role_mapping):
	"""takes an array of overwrites objects
	and replaces the roles inside according to role_mapping
	"""
	new_overwrites = {}
	for o in overwrites:
		new_overwrites[role_mapping[o]] = overwrites[o]

	return new_overwrites


async def clone_server_channels(dstguild, srcguild, role_mapping):
	"""clones the channels of srcguild into dstguild.
	returns a mapping of the source guild's chanenls
	to the corresponding channel in the destination server."""
	mapping = {}
	categories = {}
	for channel in srcguild.channels:
		if type(channel) == discord.CategoryChannel:
			logger.info(f'creating category {channel}')
			ctg = await dstguild.create_category(
				channel.name,
				overwrites=channel.overwrites,
				position=channel.position
			)
			categories[channel.id] = ctg
			mapping[channel] = ctg

	for channel in srcguild.channels:
		overwrites = convert_overwrites(channel.overwrites, role_mapping)
		if type(channel) == discord.TextChannel:
			logger.info(f'creating text channel {channel}')
			ch = await dstguild.create_text_channel(
				channel.name,
				overwrites=overwrites,
				position=channel.position,
				category=categories[channel.category.id]
			)
			mapping[channel] = ch
		elif type(channel) == discord.VoiceChannel:
			logger.info(f'creating voice channel {channel}')
			ch = await dstguild.create_voice_channel(
				channel.name,
				overwrites=overwrites,
				position=channel.position,
				category=categories[channel.category.id]
			)
			mapping[channel] = ch

	return mapping


class Cog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.mappings = []

	def get_mapping(self, srv1, srv2):
		for m in self.mappings:
			if m.contains(srv1, srv2):
				return m
		return None

	@commands.command()
	async def clone(self, ctx, gid: int):
		"""clones the specified server id"""
		dstguild = ctx.guild
		srcguild = self.bot.get_guild(gid)
		if not srcguild:
			raise commands.UserInputError(
				message=f'guild with id {gid} not accessible or nonexistent'
			)


		roles = await clone_server_roles(dstguild, srcguild)
		channels = await clone_server_channels(dstguild, srcguild, roles)
		self.mappings.append(GuildMapping(srcguild, dstguild, roles, channels))
		logger.debug(f'mappings consists of: {self.mappings}')



