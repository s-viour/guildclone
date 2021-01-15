import discord
import traceback
import sys
from discord.ext import commands


# wonderful error handling module
# retrieved from https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')

        elif isinstance(error, commands.UserInputError):
            await ctx.send(f'Error in command input: {error}')

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


class GuildMapping:
    """class that represents a mapping of roles and channels
    from one guild to another. contains a bunch of helper functions
    for creating dictionaries of roles and channels from one server to another
    """
    def __init__(self, src, dst, role_mapping, channel_mapping):
        self.role_mapping = role_mapping
        self.channel_mapping = channel_mapping
        self.srcguild = src
        self.dstguild = dst
        logger.debug('mapping created:')
        logger.debug(f'srcguild: {self.srcguild.id} dstguild: {self.dstguild.id}')

    @property
    def src(self):
        return self.srcguild

    @property
    def dst(self):
        return self.dstguild

    def contains(self, srv1, srv2):
        """determines if the two supplied servers
        are the srcguild and dstguild in this mapping"""
        c1 = srv1 == self.srcguild and srv2 == self.dstguild
        c2 =  srv2 == self.srcguild and srv1 == self.dstguild
        return c1 or c2

    # helper functions for generating mappings to or from guilds
    def role_src_to_dst(self):
        return self.role_mapping

    def role_dst_to_src(self):
        return { v: k for k, v in self.role_mapping.items() }

    def channel_src_to_dest(self):
        return self.channel_mapping

    def channel_dst_to_src(self):
        return { v: k for k, v in self.channel_mapping.items() }