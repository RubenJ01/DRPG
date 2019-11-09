from utils.database.db_functions import GUILD_SETTINGS
from utils.database import db_functions as db


def is_empty(structure):
    if structure:
        # structure is not empty return false
        return False
    else:
        # structure is empty return true
        return True


def get_prefix(bot, message):
    if not message.guild:
        return bot.config["prefix"]
    try:
        prefix = GUILD_SETTINGS[message.guild.id]
    except KeyError:
        prefix = bot.config["prefix"]

    return prefix


async def has_job(job, user_id):
    db_connection = await db.dbconnection()
    cursor = await db_connection.cursor()
    sql = "SELECT job FROM jobs WHERE current_job = %s AND character_id = '%s' AND job = %s"
    val = ('true', user_id, job)
    await cursor.execute(sql, val)
    result = await cursor.fetchall()
    await cursor.close()
    db_connection.close()
    if is_empty(result):
        # returns false because the users doesnt have a job
        return False
    else:
        # returns true because the user has a job
        return True

