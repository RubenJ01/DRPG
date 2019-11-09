import aiomysql
import logging
import yaml
from pathlib import Path


logger = logging.getLogger('bot.' + __name__)


GUILD_SETTINGS = {}


async def dbconnection():
    """Connect to database and return connection object."""
    NAMEFILE = Path('config.yaml')

    with open(NAMEFILE, encoding='utf8') as f:
        data = yaml.safe_load(f)
    try:
        db_connection = await aiomysql.connect(
            host=data['database']['host'],
            user=data['database']['user'],
            password=data['database']['passwd'],
            db=data['database']['database']
        )
    except Exception as e:
        logger.error(f"DB CONNECTION ERROR:\n{str(e)}")
    return db_connection


async def sql_query(sql_code, values=()):
    """A function used to make database queries."""
    conn = await dbconnection()
    async with conn.cursor() as cur:
        try:
            await cur.execute(sql_code, values)
        except Exception as e:
            logger.error(f"ERROR WHILE EXECUTING SQL:\n{str(e)}")
            results = []
            conn.close()
            return results
        else:
            results = await cur.fetchall()
            conn.close()
            return results
    

async def sql_edit(sql_code, values=()):
    """A function used to make database queries."""
    conn = await dbconnection()
    async with conn.cursor() as cur:
        try:
            await cur.execute(sql_code, values)
        except Exception as e:
            logger.error(f"ERROR WHILE EXECUTING SQL:\n{str(e)}")
            await conn.commit()
            conn.close()
            return False
        else:
            await conn.commit()
            conn.close()
            return True
    

async def cache_prefixes():
    """Cache all prefixes."""
    logger.info("Caching prefixes...")
    sql = "select * from guild_settings"
    results = await sql_query(sql)
    for result in results:
        GUILD_SETTINGS[result[0]] = result[1]
    print(GUILD_SETTINGS)
    logger.info("Caching prefixes done!")
