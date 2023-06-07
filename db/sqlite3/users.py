# from db.sqlite3.connect import SQLConnection
from connect import SQLConnection

from nextcord import Member, User

from typing import Union

def add_user(bot, discord_user: Union[Member, int], mc_uuid: str) -> Union[None, list[set]]:
    discord_id = discord_user.id if isinstance(discord_user, Member) else discord_user
    
    database = SQLConnection()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM users WHERE mc_uuid=?", (mc_uuid,))
    dupes = cursor.fetchall()

    if len(dupes) > 0:
        return dupes

    cursor.execute("INSERT INTO users(discord_id, mc_uuid) VALUES (?, ?)", (discord_id, mc_uuid))

    database.commit()
    cursor.close()

def get_user_by_uuid(mc_uuid: str) -> list:
    database = SQLConnection()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM users WHERE mc_uuid=?", (mc_uuid,))
    results = cursor.fetchall()
    cursor.close()

    return results

def get_user_by_discord(bot, discord_user: Union[int, Member, User]):
    discord_id = discord_user.id if isinstance(discord_user, Member) or isinstance(discord_user, User) else discord_user

    database = SQLConnection()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM users WHERE discord_id=?", (discord_id,))
    result = cursor.fetchall()
    cursor.close()

    return result


add_user(123234, "bread")