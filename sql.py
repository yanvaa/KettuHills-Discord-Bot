from mysql.connector import connect
from contextlib import closing
from config import sql_config

def get_moontime():
    with closing(connect(**sql_config)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM moonphase WHERE `id`=1")
            result = cursor.fetchall()
            if result != []:
                return result[0]
            else:
                return None

def get_form(id):
    with closing(connect(**sql_config)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM forms WHERE `id`=%s", (id,))
            result = cursor.fetchall()
            if result != []:
                return result[0]
            else:
                return None

def new_form(id, discord, nickname, gender, reason, motivation, message):
    with closing(connect(**sql_config)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("INSERT INTO forms (id, discord, nickname, gender, reason, motivation, message) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                           (id, discord, nickname, gender, reason, motivation, message, ))
            connection.commit()
            return True
    return False

def get_thread(channelid):
    with closing(connect(**sql_config)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM thread WHERE `channelid`=%s", (channelid,))
            result = cursor.fetchall()
            if result != []:
                return result[0]
            else:
                return None

def new_thread(channelid, threadname):
    with closing(connect(**sql_config)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("INSERT INTO thread (channelid, threadname) VALUES (%s, %s)", (channelid, threadname, ))
            connection.commit()
            return True
    return False
            
def delete_thread(channelid):
    with closing(connect(**sql_config)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("DELETE FROM thread WHERE `channelid`=%s", (channelid, ))
            connection.commit()
            return True
    return False

def new_reaction(channelid, emoji):
    with closing(connect(**sql_config)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("INSERT INTO reaction (channelid, emoji) VALUES (%s, %s)", (channelid, emoji, ))
            connection.commit()
            return True
    return False

def get_reaction(channelid):
    with closing(connect(**sql_config)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM reaction WHERE `channelid`=%s", (channelid,))
            result = cursor.fetchall()
            if result != []:
                return result[0]
            else:
                return None
            
def delete_reaction(channelid):
    with closing(connect(**sql_config)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("DELETE FROM reaction WHERE `channelid`=%s", (channelid, ))
            connection.commit()
            return True
    return False

def get_work(message):
    with closing(connect(**sql_config)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM works WHERE `message`=%s", (message,))
            result = cursor.fetchall()
            if result != []:
                return result[0]
            else:
                return None
            
def new_work(message, type, description, worker, max_worker):
    with closing(connect(**sql_config)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("INSERT INTO works (message, type, description, worker, max_worker, members) VALUES (%s, %s, %s, %s, %s, \"\")", (message, type, description, worker, max_worker, ))
            connection.commit()

def update_work(message, worker, members):
    with closing(connect(**sql_config)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("UPDATE works SET `worker`=%s, `members`=%s WHERE `message` = %s", (worker, members, message, ))
            connection.commit()