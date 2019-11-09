from utils.functions_ import is_empty
from utils.database import db_functions as db

from discord.ext import commands
from discord.ext.commands import check

bot_admin = 391583287652515841


class NotBotAdmin(commands.CheckFailure):
    """Exception raised when an admin command is used by a non admin user"""
    pass


class NoCharacter(commands.CheckFailure):
    """Exception raised when a command is used by user without a character"""
    pass


def is_admin():
    def predicate(ctx):
        if ctx.author.id != bot_admin:
            raise NotBotAdmin
        return True

    return check(predicate)


def has_character():
    async def predicate(ctx):
        user_id = ctx.author.id
        db_connection = await db.dbconnection()
        cursor = await db_connection.cursor()
        sql = "SELECT `name` FROM `character` WHERE user_id = '%s'"
        val = user_id
        await cursor.execute(sql, (val,))
        result = await cursor.fetchall()
        await cursor.close()
        db_connection.close()
        if is_empty(result):
            raise NoCharacter
        else:
            # returns true because the users has a character
            return True
    return check(predicate)
