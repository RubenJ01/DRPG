import logging

import discord
from discord.ext import commands

from utils.database import db_functions as db

logger = logging.getLogger(f"bot.{__name__}")


class GuildSettings(commands.Cog):
    """A cog for managing guild settings."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='prefix')
    @commands.has_permissions(manage_guild=True)
    async def set_prefix(self, ctx, new_prefix: str) -> None:
        """Set a new prefix for the bot in this server."""
        sql = "UPDATE guild_settings SET prefix=%s where guild_id=%s"
        values = (new_prefix, ctx.guild.id)
        status = await db.sql_edit(sql, values)
        await db.cache_prefixes()
        if status:
            await ctx.send(f"Prefix has been updated to {new_prefix}")
        else:
            await ctx.send("Prefix could not be changed.")


def setup(bot):
    bot.add_cog(GuildSettings(bot))
    logger.info("loaded")
